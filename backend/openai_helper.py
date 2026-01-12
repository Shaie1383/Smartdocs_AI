import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIHelper:
    
    def __init__(self):

        self.api_key = None
        self.client = None
        self.load_api_key()
    
    def load_api_key(self) -> bool:
        
        try:
            load_dotenv()
    
            self.api_key = os.getenv('OPENAI_API_KEY')
            
            if not self.api_key:
                logger.error("OPENAI_API_KEY not found in .env file")
                return False
            
            if not self.api_key.startswith('sk-'):
                logger.error("Invalid API key format. OpenAI API keys should start with 'sk-'")
                return False
            
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI API key loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading API key: {str(e)}")
            return False
    
    def test_connection(self) -> Dict[str, Any]:
        
        if not self.client:
            return {
                "success": False,
                "error": "API client not initialized. Please check your API key."
            }
        
        try:
        
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello, are you working?"}
                ],
                max_tokens=50,
                temperature=0.7
            )
            

            message_content = response.choices[0].message.content
            
            logger.info("API connection test successful")
            return {
                "success": True,
                "response": message_content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                }
            }
            
        except Exception as e:
            error_message = str(e)
            
            # Handle specific error types
            if "invalid_api_key" in error_message.lower() or "incorrect api key" in error_message.lower():
                return {
                    "success": False,
                    "error": "Invalid API key. Please check your OPENAI_API_KEY in .env file.",
                    "error_type": "authentication_error"
                }
            
            elif "rate_limit" in error_message.lower():
                return {
                    "success": False,
                    "error": "Rate limit exceeded. Please wait a moment and try again.",
                    "error_type": "rate_limit_error"
                }
            
            elif "insufficient_quota" in error_message.lower() or "quota" in error_message.lower():
                return {
                    "success": False,
                    "error": "Insufficient credits. Please check your OpenAI account balance.",
                    "error_type": "quota_error"
                }
            
            elif "timeout" in error_message.lower() or "connection" in error_message.lower():
                return {
                    "success": False,
                    "error": "Network error. Please check your internet connection and try again.",
                    "error_type": "network_error"
                }
            
            else:
                logger.error(f"API test failed: {error_message}")
                return {
                    "success": False,
                    "error": f"API error: {error_message}",
                    "error_type": "unknown_error"
                }
    
    def get_completion(
        self, 
        prompt: str, 
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get completion from OpenAI API
        
        Args:
            prompt: User prompt/question
            model: OpenAI model to use (default: gpt-3.5-turbo)
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)
            system_message: Optional system message to set context
            
        Returns:
            Dict containing response or error information
        """
        if not self.client:
            return {
                "success": False,
                "error": "API client not initialized. Please check your API key."
            }
        
        try:
            # Prepare messages
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            # Make API call using new API (openai >= 1.0.0)
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract response
            message_content = response.choices[0].message.content
            
            return {
                "success": True,
                "response": message_content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                },
                "finish_reason": response.choices[0].finish_reason
            }
            
        except Exception as e:
            error_message = str(e)
            
            # Handle specific error types
            if "invalid_api_key" in error_message.lower() or "incorrect api key" in error_message.lower():
                return {
                    "success": False,
                    "error": "Invalid API key. Please check your OPENAI_API_KEY in .env file.",
                    "error_type": "authentication_error"
                }
            
            elif "rate_limit" in error_message.lower():
                return {
                    "success": False,
                    "error": "Rate limit exceeded. Please wait a moment and try again.",
                    "error_type": "rate_limit_error"
                }
            
            elif "insufficient_quota" in error_message.lower() or "quota" in error_message.lower():
                return {
                    "success": False,
                    "error": "Insufficient credits. Please check your OpenAI account balance.",
                    "error_type": "quota_error"
                }
            
            elif "timeout" in error_message.lower() or "connection" in error_message.lower():
                return {
                    "success": False,
                    "error": "Network error. Please check your internet connection and try again.",
                    "error_type": "network_error"
                }
            
            elif "model" in error_message.lower() and "does not exist" in error_message.lower():
                return {
                    "success": False,
                    "error": f"Model '{model}' not found. Please use a valid model name.",
                    "error_type": "invalid_model_error"
                }
            
            else:
                logger.error(f"API call failed: {error_message}")
                return {
                    "success": False,
                    "error": f"API error: {error_message}",
                    "error_type": "unknown_error"
                }


# Standalone functions for backward compatibility
def load_api_key() -> bool:
    """
    Load and validate OpenAI API key from .env file
    
    Returns:
        bool: True if successful, False otherwise
    """
    helper = OpenAIHelper()
    return helper.api_key is not None


def test_connection() -> Dict[str, Any]:
    """
    Test OpenAI API connection
    
    Returns:
        Dict with test results
    """
    helper = OpenAIHelper()
    return helper.test_connection()


def get_completion(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 500,
    temperature: float = 0.7,
    system_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get completion from OpenAI API
    
    Args:
        prompt: User prompt
        model: Model name
        max_tokens: Max response tokens
        temperature: Creativity (0-1)
        system_message: Optional system context
        
    Returns:
        Dict with response or error
    """
    helper = OpenAIHelper()
    return helper.get_completion(prompt, model, max_tokens, temperature, system_message)
