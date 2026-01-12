"""
Text Chunking Module
Handles intelligent text segmentation for document processing
"""

import re
import tiktoken
from typing import List, Dict, Any, Optional
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextChunker:
    """
    Advanced text chunking class that splits documents into smaller,
    manageable pieces while preserving context and semantic meaning.
    """
    
    def __init__(self, 
                 chunk_size: int = 1000, 
                 chunk_overlap: int = 200,
                 encoding_name: str = "cl100k_base"):
        """
        Initialize TextChunker with configurable parameters
        
        Args:
            chunk_size (int): Maximum tokens per chunk (default: 1000)
            chunk_overlap (int): Token overlap between chunks (default: 200)
            encoding_name (str): Tiktoken encoding name (default: cl100k_base for GPT-3.5/4)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding_name = encoding_name
        
        # Initialize tokenizer
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
            logger.info(f"TextChunker initialized with encoding: {encoding_name}")
        except Exception as e:
            logger.warning(f"Failed to load encoding {encoding_name}, falling back to cl100k_base: {e}")
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string
        
        Args:
            text (str): Input text
            
        Returns:
            int: Number of tokens
        """
        if not text:
            return 0
        return len(self.encoding.encode(text))
    
    def chunk_by_tokens(self, 
                       text: str, 
                       chunk_size: Optional[int] = None,
                       chunk_overlap: Optional[int] = None) -> List[str]:
        """
        Split text into fixed-size chunks based on token count with overlap
        
        Args:
            text (str): Input text to chunk
            chunk_size (int, optional): Override default chunk size
            chunk_overlap (int, optional): Override default overlap size
            
        Returns:
            List[str]: List of text chunks
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []
        
        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap
        
        # Encode text into tokens
        tokens = self.encoding.encode(text)
        total_tokens = len(tokens)
        
        logger.info(f"Chunking {total_tokens} tokens with size={chunk_size}, overlap={chunk_overlap}")
        
        chunks = []
        start_idx = 0
        
        while start_idx < total_tokens:
            # Get chunk tokens
            end_idx = min(start_idx + chunk_size, total_tokens)
            chunk_tokens = tokens[start_idx:end_idx]
            
            # Decode tokens back to text
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
            
            # Move to next chunk with overlap
            if end_idx >= total_tokens:
                break
            
            start_idx += chunk_size - chunk_overlap
        
        logger.info(f"Created {len(chunks)} token-based chunks")
        return chunks
    
    def chunk_by_sentences(self, text: str, max_chunk_size: Optional[int] = None) -> List[str]:
        """
        Split text into chunks while preserving sentence boundaries
        
        Args:
            text (str): Input text to chunk
            max_chunk_size (int, optional): Maximum tokens per chunk
            
        Returns:
            List[str]: List of text chunks preserving sentences
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for sentence chunking")
            return []
        
        max_chunk_size = max_chunk_size or self.chunk_size
        
        # Split text into sentences using regex
        # This pattern handles common sentence endings: . ! ?
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(sentence_pattern, text)
        
        # If no sentences found, treat as single sentence
        if not sentences:
            sentences = [text]
        
        logger.info(f"Found {len(sentences)} sentences to chunk")
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_tokens = self.count_tokens(sentence)
            
            # If single sentence exceeds max size, split it by tokens
            if sentence_tokens > max_chunk_size:
                # Save current chunk if exists
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                    current_tokens = 0
                
                # Split large sentence
                large_chunks = self.chunk_by_tokens(sentence, chunk_size=max_chunk_size)
                chunks.extend(large_chunks)
                continue
            
            # Check if adding sentence exceeds limit
            if current_tokens + sentence_tokens > max_chunk_size and current_chunk:
                # Save current chunk and start new one
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
                current_tokens = sentence_tokens
            else:
                # Add sentence to current chunk
                current_chunk += sentence + " "
                current_tokens += sentence_tokens
        
        # Add remaining chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        logger.info(f"Created {len(chunks)} sentence-based chunks")
        return chunks
    
    def create_chunks(self,
                     text: str,
                     source_file: str,
                     page_number: Optional[int] = None,
                     chunking_strategy: str = "tokens") -> List[Dict[str, Any]]:
        """
        Create structured chunks with metadata
        
        Args:
            text (str): Input text to chunk
            source_file (str): Name of source PDF file
            page_number (int, optional): Page number in source document
            chunking_strategy (str): "tokens" or "sentences" (default: "tokens")
            
        Returns:
            List[Dict]: List of chunk dictionaries with metadata
        """
        if not text or not text.strip():
            logger.warning(f"Empty text from {source_file}, page {page_number}")
            return []
        
        # Choose chunking strategy
        if chunking_strategy == "sentences":
            raw_chunks = self.chunk_by_sentences(text)
        else:
            raw_chunks = self.chunk_by_tokens(text)
        
        # Create structured chunks with metadata
        structured_chunks = []
        for idx, chunk_text in enumerate(raw_chunks):
            chunk_data = {
                "chunk_id": str(uuid.uuid4()),  # Unique identifier
                "text": chunk_text,
                "chunk_index": idx,  # Position in document
                "source_file": source_file,
                "page_number": page_number,
                "token_count": self.count_tokens(chunk_text),
                "character_count": len(chunk_text),
                "word_count": len(chunk_text.split()),
                "chunking_strategy": chunking_strategy
            }
            structured_chunks.append(chunk_data)
        
        logger.info(f"Created {len(structured_chunks)} structured chunks from {source_file}")
        return structured_chunks
    
    def calculate_optimal_chunk_size(self, document_length: int) -> int:
        """
        Calculate optimal chunk size based on document length
        
        Args:
            document_length (int): Total tokens in document
            
        Returns:
            int: Recommended chunk size
        """
        # Strategy: Adjust chunk size based on document length
        # Short documents: smaller chunks for precision
        # Long documents: larger chunks for efficiency
        
        if document_length <= 2000:  # Short document (< 2K tokens)
            optimal_size = 500
        elif document_length <= 10000:  # Medium document (2K-10K tokens)
            optimal_size = 1000
        elif document_length <= 50000:  # Long document (10K-50K tokens)
            optimal_size = 1500
        else:  # Very long document (> 50K tokens)
            optimal_size = 2000
        
        logger.info(f"Document length: {document_length} tokens → Optimal chunk size: {optimal_size}")
        return optimal_size
    
    def merge_small_chunks(self, 
                          chunks: List[Dict[str, Any]], 
                          min_chunk_size: int = 100) -> List[Dict[str, Any]]:
        """
        Merge chunks that are too small into neighboring chunks
        
        Args:
            chunks (List[Dict]): List of chunk dictionaries
            min_chunk_size (int): Minimum acceptable chunk size in tokens
            
        Returns:
            List[Dict]: Merged chunks
        """
        if not chunks:
            return []
        
        merged_chunks = []
        i = 0
        
        while i < len(chunks):
            current_chunk = chunks[i]
            
            # If chunk is large enough, keep it
            if current_chunk["token_count"] >= min_chunk_size:
                merged_chunks.append(current_chunk)
                i += 1
                continue
            
            # If chunk is too small, try to merge with next chunk
            if i + 1 < len(chunks):
                next_chunk = chunks[i + 1]
                
                # Merge chunks
                merged_text = current_chunk["text"] + " " + next_chunk["text"]
                merged_chunk = {
                    "chunk_id": str(uuid.uuid4()),
                    "text": merged_text,
                    "chunk_index": current_chunk["chunk_index"],
                    "source_file": current_chunk["source_file"],
                    "page_number": current_chunk["page_number"],
                    "token_count": self.count_tokens(merged_text),
                    "character_count": len(merged_text),
                    "word_count": len(merged_text.split()),
                    "chunking_strategy": f"{current_chunk['chunking_strategy']}_merged"
                }
                
                merged_chunks.append(merged_chunk)
                i += 2  # Skip next chunk since it's merged
            else:
                # Last chunk is small, keep it anyway
                merged_chunks.append(current_chunk)
                i += 1
        
        logger.info(f"Merged {len(chunks)} chunks into {len(merged_chunks)} chunks")
        return merged_chunks
    
    def chunk_document(self,
                      text: str,
                      source_file: str,
                      page_number: Optional[int] = None,
                      auto_optimize: bool = True) -> List[Dict[str, Any]]:
        """
        Convenience method to chunk a document with automatic optimization
        
        Args:
            text (str): Input text
            source_file (str): Source file name
            page_number (int, optional): Page number
            auto_optimize (bool): Automatically optimize chunk size and merge small chunks
            
        Returns:
            List[Dict]: Structured chunks with metadata
        """
        if not text or not text.strip():
            return []
        
        # Auto-optimize chunk size if enabled
        if auto_optimize:
            doc_tokens = self.count_tokens(text)
            optimal_size = self.calculate_optimal_chunk_size(doc_tokens)
            self.chunk_size = optimal_size
        
        # Create chunks
        chunks = self.create_chunks(
            text=text,
            source_file=source_file,
            page_number=page_number,
            chunking_strategy="sentences"  # Default to sentence-based for better semantic coherence
        )
        
        # Merge small chunks if optimization enabled
        if auto_optimize and chunks:
            min_size = max(100, self.chunk_size // 10)  # Minimum 10% of chunk size
            chunks = self.merge_small_chunks(chunks, min_chunk_size=min_size)
        
        return chunks
    
    def chunk_multiple_pages(self, 
                            pages_dict: Dict[int, str],
                            source_file: str,
                            auto_optimize: bool = True) -> List[Dict[str, Any]]:
        """
        Chunk multiple pages from a PDF document
        
        Args:
            pages_dict (Dict[int, str]): Dictionary mapping page numbers to text content
            source_file (str): Source PDF file name
            auto_optimize (bool): Enable automatic optimization
            
        Returns:
            List[Dict]: All chunks from all pages with metadata
        """
        all_chunks = []
        
        for page_num, page_text in pages_dict.items():
            if not page_text or not page_text.strip():
                logger.warning(f"Skipping empty page {page_num} in {source_file}")
                continue
            
            page_chunks = self.chunk_document(
                text=page_text,
                source_file=source_file,
                page_number=page_num,
                auto_optimize=auto_optimize
            )
            
            all_chunks.extend(page_chunks)
        
        logger.info(f"Chunked {len(pages_dict)} pages into {len(all_chunks)} total chunks")
        return all_chunks
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics about chunks
        
        Args:
            chunks (List[Dict]): List of chunk dictionaries
            
        Returns:
            Dict: Statistics about the chunks
        """
        if not chunks:
            return {
                "total_chunks": 0,
                "total_tokens": 0,
                "total_characters": 0,
                "total_words": 0,
                "avg_tokens_per_chunk": 0,
                "avg_chars_per_chunk": 0,
                "avg_words_per_chunk": 0,
                "min_tokens": 0,
                "max_tokens": 0
            }
        
        total_tokens = sum(c["token_count"] for c in chunks)
        total_chars = sum(c["character_count"] for c in chunks)
        total_words = sum(c["word_count"] for c in chunks)
        token_counts = [c["token_count"] for c in chunks]
        
        stats = {
            "total_chunks": len(chunks),
            "total_tokens": total_tokens,
            "total_characters": total_chars,
            "total_words": total_words,
            "avg_tokens_per_chunk": round(total_tokens / len(chunks), 2),
            "avg_chars_per_chunk": round(total_chars / len(chunks), 2),
            "avg_words_per_chunk": round(total_words / len(chunks), 2),
            "min_tokens": min(token_counts),
            "max_tokens": max(token_counts)
        }
        
        return stats


# Standalone convenience functions

def chunk_text(text: str, 
               chunk_size: int = 1000, 
               chunk_overlap: int = 200,
               strategy: str = "tokens") -> List[str]:
    """
    Quick function to chunk text without metadata
    
    Args:
        text (str): Input text
        chunk_size (int): Maximum tokens per chunk
        chunk_overlap (int): Token overlap between chunks
        strategy (str): "tokens" or "sentences"
        
    Returns:
        List[str]: List of text chunks
    """
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    if strategy == "sentences":
        return chunker.chunk_by_sentences(text)
    else:
        return chunker.chunk_by_tokens(text)


def count_tokens(text: str) -> int:
    """
    Quick function to count tokens in text
    
    Args:
        text (str): Input text
        
    Returns:
        int: Number of tokens
    """
    chunker = TextChunker()
    return chunker.count_tokens(text)
