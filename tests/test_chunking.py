"""
Test script for Text Chunking Module
Tests chunking functionality with documents of varying sizes
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from text_chunker import TextChunker, chunk_text, count_tokens
from pdf_processor import PDFProcessor
import json


def print_separator(title=""):
    """Print a visual separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"{title:^70}")
        print("=" * 70)


def test_token_counting():
    """Test 1: Token Counting"""
    print_separator("TEST 1: Token Counting")
    
    test_texts = [
        "Hello, world!",
        "This is a longer sentence with more words to count.",
        "The quick brown fox jumps over the lazy dog. " * 10
    ]
    
    for idx, text in enumerate(test_texts, 1):
        token_count = count_tokens(text)
        word_count = len(text.split())
        print(f"\nText {idx}:")
        print(f"  Content: {text[:60]}...")
        print(f"  Words: {word_count}")
        print(f"  Tokens: {token_count}")
        print(f"  Ratio: {token_count/word_count:.2f} tokens per word")


def test_fixed_token_chunking():
    """Test 2: Fixed-Size Token Chunking"""
    print_separator("TEST 2: Fixed-Size Token Chunking")
    
    # Create a long text
    text = """
    Artificial Intelligence (AI) is transforming the world as we know it. 
    Machine learning algorithms can now process vast amounts of data and 
    identify patterns that humans might miss. Deep learning, a subset of 
    machine learning, uses neural networks with multiple layers to learn 
    from data in a way that mimics the human brain. Natural Language 
    Processing (NLP) enables computers to understand, interpret, and 
    generate human language. Computer vision allows machines to interpret 
    and understand visual information from the world. AI applications are 
    everywhere: from recommendation systems on streaming platforms to 
    autonomous vehicles navigating city streets. The future of AI holds 
    immense potential for solving complex problems in healthcare, climate 
    change, education, and many other fields. However, it also raises 
    important ethical questions about privacy, bias, and the impact on 
    employment. As AI continues to evolve, it's crucial that we develop 
    it responsibly and ensure it benefits all of humanity.
    """ * 5  # Repeat to create longer text
    
    chunker = TextChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_by_tokens(text)
    
    print(f"\nOriginal text tokens: {chunker.count_tokens(text)}")
    print(f"Chunk size: 200 tokens")
    print(f"Overlap: 50 tokens")
    print(f"Number of chunks created: {len(chunks)}")
    
    for idx, chunk in enumerate(chunks[:3], 1):  # Show first 3 chunks
        print(f"\n--- Chunk {idx} ---")
        print(f"Tokens: {chunker.count_tokens(chunk)}")
        print(f"Preview: {chunk[:100]}...")


def test_sentence_chunking():
    """Test 3: Sentence-Based Chunking"""
    print_separator("TEST 3: Sentence-Based Chunking")
    
    text = """
    Climate change is one of the most pressing issues of our time. Rising 
    global temperatures are causing ice caps to melt. Sea levels are 
    increasing, threatening coastal communities. Extreme weather events 
    are becoming more frequent and severe. Scientists agree that human 
    activity is the primary driver. Greenhouse gas emissions from burning 
    fossil fuels are the main culprit. Deforestation also contributes 
    significantly to the problem. We must take immediate action to reduce 
    emissions. Renewable energy sources like solar and wind power offer 
    hope. Individual actions matter too. Reducing waste, conserving energy, 
    and supporting sustainable practices can make a difference. The time 
    to act is now!
    """ * 3
    
    chunker = TextChunker(chunk_size=150, chunk_overlap=30)
    chunks = chunker.chunk_by_sentences(text)
    
    print(f"\nOriginal text tokens: {chunker.count_tokens(text)}")
    print(f"Max chunk size: 150 tokens")
    print(f"Number of chunks created: {len(chunks)}")
    
    for idx, chunk in enumerate(chunks[:3], 1):
        print(f"\n--- Chunk {idx} ---")
        print(f"Tokens: {chunker.count_tokens(chunk)}")
        print(f"Sentences: {chunk.count('.')}")
        print(f"Content: {chunk[:120]}...")


def test_structured_chunks():
    """Test 4: Structured Chunks with Metadata"""
    print_separator("TEST 4: Structured Chunks with Metadata")
    
    text = "This is page 1 content. " * 50
    
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.create_chunks(
        text=text,
        source_file="test_document.pdf",
        page_number=1,
        chunking_strategy="tokens"
    )
    
    print(f"\nCreated {len(chunks)} structured chunks")
    
    # Show first chunk details
    if chunks:
        print("\n--- Sample Chunk Metadata ---")
        chunk = chunks[0]
        print(json.dumps(chunk, indent=2, default=str))


def test_optimal_chunk_size():
    """Test 5: Optimal Chunk Size Calculation"""
    print_separator("TEST 5: Optimal Chunk Size Calculation")
    
    chunker = TextChunker()
    
    test_lengths = [1000, 5000, 15000, 60000, 100000]
    
    print("\nDocument Length → Optimal Chunk Size:")
    for length in test_lengths:
        optimal = chunker.calculate_optimal_chunk_size(length)
        print(f"  {length:>7,} tokens → {optimal:>5} tokens per chunk")


def test_merge_small_chunks():
    """Test 6: Merging Small Chunks"""
    print_separator("TEST 6: Merging Small Chunks")
    
    # Create some small chunks manually
    small_chunks = [
        {
            "chunk_id": "1",
            "text": "Small chunk 1",
            "chunk_index": 0,
            "source_file": "test.pdf",
            "page_number": 1,
            "token_count": 30,
            "character_count": 13,
            "word_count": 3,
            "chunking_strategy": "tokens"
        },
        {
            "chunk_id": "2",
            "text": "Small chunk 2",
            "chunk_index": 1,
            "source_file": "test.pdf",
            "page_number": 1,
            "token_count": 40,
            "character_count": 13,
            "word_count": 3,
            "chunking_strategy": "tokens"
        },
        {
            "chunk_id": "3",
            "text": "Large chunk with lots of content " * 20,
            "chunk_index": 2,
            "source_file": "test.pdf",
            "page_number": 1,
            "token_count": 500,
            "character_count": 660,
            "word_count": 120,
            "chunking_strategy": "tokens"
        }
    ]
    
    chunker = TextChunker()
    merged = chunker.merge_small_chunks(small_chunks, min_chunk_size=100)
    
    print(f"\nOriginal chunks: {len(small_chunks)}")
    print(f"After merging: {len(merged)}")
    print("\nMerged chunk sizes:")
    for idx, chunk in enumerate(merged, 1):
        print(f"  Chunk {idx}: {chunk['token_count']} tokens")


def test_with_real_pdf():
    """Test 7: Chunking Real PDF Documents"""
    print_separator("TEST 7: Chunking Real PDF Documents")
    
    data_dir = Path(__file__).parent.parent / "data"
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("\n⚠️  No PDF files found in data/ directory")
        print("   Run 'python generate_sample_pdfs.py' first")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s) in data/")
    
    # Test with first PDF
    pdf_path = str(pdf_files[0])
    print(f"\nProcessing: {pdf_files[0].name}")
    
    try:
        # Extract text
        processor = PDFProcessor(pdf_path)
        result = processor.extract_text_pymupdf()
        
        # Chunk the document
        chunker = TextChunker(chunk_size=500, chunk_overlap=100)
        all_chunks = chunker.chunk_multiple_pages(
            pages_dict=result["content"],
            source_file=pdf_files[0].name,
            auto_optimize=True
        )
        
        print(f"\n✅ Successfully chunked PDF:")
        print(f"   Total pages: {result['total_pages']}")
        print(f"   Total chunks: {len(all_chunks)}")
        
        # Get statistics
        stats = chunker.get_chunk_statistics(all_chunks)
        print(f"\n📊 Chunk Statistics:")
        print(f"   Total tokens: {stats['total_tokens']:,}")
        print(f"   Avg tokens/chunk: {stats['avg_tokens_per_chunk']}")
        print(f"   Min tokens: {stats['min_tokens']}")
        print(f"   Max tokens: {stats['max_tokens']}")
        print(f"   Total words: {stats['total_words']:,}")
        
        # Show sample chunk
        if all_chunks:
            print(f"\n--- Sample Chunk (Chunk 1) ---")
            chunk = all_chunks[0]
            print(f"Source: {chunk['source_file']} (Page {chunk['page_number']})")
            print(f"Tokens: {chunk['token_count']}")
            print(f"Preview: {chunk['text'][:200]}...")
        
    except Exception as e:
        print(f"\n❌ Error processing PDF: {e}")


def test_different_document_sizes():
    """Test 8: Chunking Documents of Different Sizes"""
    print_separator("TEST 8: Different Document Sizes")
    
    # Short document (< 2 pages)
    short_text = "This is a short document. " * 100
    
    # Medium document (~ 20 pages worth)
    medium_text = "This is a medium-length document with various content. " * 2000
    
    # Long document (~ 100 pages worth)
    long_text = "This is a very long document with extensive content. " * 10000
    
    documents = [
        ("Short (2-page)", short_text),
        ("Medium (20-page)", medium_text),
        ("Long (100-page)", long_text)
    ]
    
    print("\nDocument Type | Tokens | Optimal Size | Chunks Created")
    print("-" * 65)
    
    for doc_type, text in documents:
        chunker = TextChunker()
        token_count = chunker.count_tokens(text)
        optimal_size = chunker.calculate_optimal_chunk_size(token_count)
        
        # Chunk with optimal size
        chunker.chunk_size = optimal_size
        chunks = chunker.chunk_by_tokens(text)
        
        print(f"{doc_type:15} | {token_count:>6,} | {optimal_size:>12} | {len(chunks):>14}")


def run_all_tests():
    """Run all chunking tests"""
    print("\n" + "=" * 70)
    print("TEXT CHUNKING MODULE - COMPREHENSIVE TEST SUITE".center(70))
    print("=" * 70)
    
    tests = [
        ("Token Counting", test_token_counting),
        ("Fixed Token Chunking", test_fixed_token_chunking),
        ("Sentence Chunking", test_sentence_chunking),
        ("Structured Chunks", test_structured_chunks),
        ("Optimal Chunk Size", test_optimal_chunk_size),
        ("Merge Small Chunks", test_merge_small_chunks),
        ("Real PDF Chunking", test_with_real_pdf),
        ("Different Document Sizes", test_different_document_sizes)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"\n✅ {test_name} - PASSED")
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} - FAILED")
            print(f"   Error: {e}")
    
    # Summary
    print_separator("TEST SUMMARY")
    print(f"\nTotal Tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"\nSuccess Rate: {(passed/len(tests)*100):.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! Text chunking module is working perfectly!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")


if __name__ == "__main__":
    run_all_tests()
