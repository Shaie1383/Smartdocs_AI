"""
Test script for OpenAI API integration
Demonstrates API connectivity and basic functionality
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from openai_helper import OpenAIHelper


def print_separator(title=""):
    """Print a formatted separator"""
    print("\n" + "=" * 70)
    if title:
        print(f"  {title}")
        print("=" * 70)
    print()


def test_api_integration():
    """Test OpenAI API integration"""
    
    print_separator("OPENAI API INTEGRATION TEST")
    
    # Initialize helper
    print("1️⃣  Initializing OpenAI Helper...")
    helper = OpenAIHelper()
    
    if not helper.api_key:
        print("❌ Failed to load API key!")
        print("   Please check your .env file contains OPENAI_API_KEY")
        return False
    
    print("✅ API key loaded successfully")
    print(f"   Key preview: {helper.api_key[:10]}...{helper.api_key[-4:]}")
    
    # Test connection
    print_separator("2️⃣  Testing API Connection")
    print("Sending test prompt: 'Hello, are you working?'")
    print("Please wait...")
    
    result = helper.test_connection()
    
    if result["success"]:
        print("✅ API Connection Successful!")
        print(f"\n   Model: {result['model']}")
        print(f"   Response: {result['response']}")
        print(f"\n   Token Usage:")
        print(f"   - Prompt tokens: {result['usage']['prompt_tokens']}")
        print(f"   - Completion tokens: {result['usage']['completion_tokens']}")
        print(f"   - Total tokens: {result['usage']['total_tokens']}")
    else:
        print("❌ API Connection Failed!")
        print(f"   Error Type: {result.get('error_type', 'unknown')}")
        print(f"   Error: {result['error']}")
        return False
    
    # Test custom completion
    print_separator("3️⃣  Testing Custom Completion")
    
    test_prompts = [
        {
            "prompt": "What is SmartDocs AI?",
            "system": "You are a helpful assistant for a PDF processing application."
        },
        {
            "prompt": "Explain text extraction in 2 sentences.",
            "system": None
        }
    ]
    
    for idx, test in enumerate(test_prompts, 1):
        print(f"\nTest {idx}: {test['prompt']}")
        if test['system']:
            print(f"System: {test['system']}")
        
        result = helper.get_completion(
            prompt=test['prompt'],
            system_message=test['system'],
            max_tokens=150,
            temperature=0.7
        )
        
        if result["success"]:
            print(f"✅ Response: {result['response']}")
            print(f"   Tokens used: {result['usage']['total_tokens']}")
        else:
            print(f"❌ Error: {result['error']}")
    
    # Summary
    print_separator("✅ TEST SUMMARY")
    print("All tests completed successfully!")
    print("\nOpenAI API Integration Status: READY ✅")
    print("\nYou can now use the following functions:")
    print("  - load_api_key()       : Load and validate API key")
    print("  - test_connection()    : Test API connectivity")
    print("  - get_completion()     : Get AI responses")
    print_separator()
    
    return True


if __name__ == "__main__":
    try:
        success = test_api_integration()
        
        if success:
            print("\n🎉 OpenAI API integration is working perfectly!")
            sys.exit(0)
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
