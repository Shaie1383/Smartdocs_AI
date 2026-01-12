# OpenAI API Setup Guide

This guide provides step-by-step instructions for obtaining and configuring your OpenAI API key for SmartDocs AI.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Creating an OpenAI Account](#creating-an-openai-account)
3. [Generating an API Key](#generating-an-api-key)
4. [Configuring the API Key](#configuring-the-api-key)
5. [Testing the API Connection](#testing-the-api-connection)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Prerequisites

Before you begin, ensure you have:
- ✅ A valid email address
- ✅ A phone number for verification
- ✅ A credit/debit card for billing (OpenAI provides free credits for new accounts)
- ✅ SmartDocs AI project set up on your local machine

---

## Creating an OpenAI Account

### Step 1: Visit OpenAI Platform
1. Navigate to [https://platform.openai.com](https://platform.openai.com)
2. Click on **"Sign Up"** in the top-right corner

### Step 2: Register Your Account
1. Choose one of the following registration methods:
   - **Email**: Enter your email and create a password
   - **Google**: Sign up with your Google account
   - **Microsoft**: Sign up with your Microsoft account

2. Verify your email address by clicking the link sent to your inbox

### Step 3: Complete Phone Verification
1. Enter your phone number
2. Enter the verification code sent via SMS
3. Complete the registration process

---

## Generating an API Key

### Step 1: Access API Keys Section
1. Log in to your OpenAI account at [https://platform.openai.com](https://platform.openai.com)
2. Click on your **profile icon** in the top-right corner
3. Select **"View API Keys"** from the dropdown menu
   - Or navigate directly to: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 2: Create a New API Key
1. Click the **"+ Create new secret key"** button
2. (Optional) Give your key a descriptive name (e.g., "SmartDocs AI Development")
3. Click **"Create secret key"**

### Step 3: Copy Your API Key
⚠️ **IMPORTANT**: This is the ONLY time you'll see the complete API key!

1. The key will be displayed in a popup window
2. Click **"Copy"** to copy the key to your clipboard
3. **Save it immediately** in a secure location (password manager recommended)
4. The key format looks like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

> **Warning**: If you lose this key, you cannot retrieve it. You'll need to create a new one.

---

## Configuring the API Key

### Step 1: Locate Your Project Directory
Navigate to your SmartDocs AI project folder:
```bash
cd "c:\Users\shais\OneDrive\Desktop\HTML\infosys springboard\Smartdocs_AI"
```

### Step 2: Create the .env File
1. In the **root directory** of the project, create a file named `.env`
2. Add the following line to the file:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

Replace `sk-proj-your-actual-api-key-here` with your actual API key copied from OpenAI.

**Example:**
```env
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Note:** Never commit your actual API key to version control!

### Step 3: Verify .gitignore
Ensure your `.env` file is listed in `.gitignore` to prevent accidentally committing your API key to version control:

```gitignore
# .gitignore
.env
```

This is **critical** for security! ✅ This is already configured in the project.

---

## Testing the API Connection

### Step 1: Activate Your Virtual Environment
```bash
# Windows
conda activate smartdocs_env

# Or if using venv
venv\Scripts\activate
```

### Step 2: Run the Test Script
```bash
python test_openai_api.py
```

### Step 3: Verify Successful Connection
You should see output similar to:

```
=====================================
OPENAI API INTEGRATION TEST
=====================================

1️⃣  Initializing OpenAI Helper...
✅ API key loaded successfully
   Key preview: sk-proj-aM...vaAA

=====================================
2️⃣  Testing API Connection
=====================================
✅ API Connection Successful!

   Model: gpt-3.5-turbo-0125
   Response: Hello! Yes, I am here to assist you. How can I help you today?
   Token Usage:
   - Prompt tokens: 13
   - Completion tokens: 18
   - Total tokens: 31

=====================================
✅ TEST SUMMARY
=====================================
All tests completed successfully!

OpenAI API Integration Status: READY ✅
```

If you see this output, **congratulations!** Your API is configured correctly. 🎉

---

## Troubleshooting

### Error: "Invalid API key"
**Problem**: The API key is incorrect or malformed.

**Solutions**:
1. Verify the key starts with `sk-proj-` or `sk-`
2. Check for extra spaces or line breaks in the `.env` file
3. Ensure you copied the complete key
4. Generate a new API key if the current one is invalid

### Error: "Rate limit exceeded"
**Problem**: You're making too many requests too quickly.

**Solutions**:
1. Wait 1-2 minutes before trying again
2. Implement rate limiting in your code
3. Consider upgrading to a paid tier for higher limits

### Error: "Insufficient quota"
**Problem**: Your account has run out of credits.

**Solutions**:
1. Check your usage at: [https://platform.openai.com/usage](https://platform.openai.com/usage)
2. Add billing information: [https://platform.openai.com/account/billing](https://platform.openai.com/account/billing)
3. Purchase additional credits
4. New accounts receive **$5 in free credits** valid for 3 months

### Error: "OPENAI_API_KEY not found in .env file"
**Problem**: The `.env` file doesn't exist or is in the wrong location.

**Solutions**:
1. Ensure `.env` is in the **root directory** of the project
2. Check the file is named exactly `.env` (not `.env.txt`)
3. Verify the format: `OPENAI_API_KEY=your-key-here` (no spaces around `=`)

### Error: "Network error"
**Problem**: Cannot connect to OpenAI servers.

**Solutions**:
1. Check your internet connection
2. Verify firewall/proxy settings
3. Try again in a few minutes
4. Check OpenAI status: [https://status.openai.com](https://status.openai.com)

---

## Best Practices

### 🔐 Security
1. **Never commit** your `.env` file to Git
2. **Never share** your API key publicly (GitHub, forums, etc.)
3. **Rotate keys** regularly (every 90 days recommended)
4. **Use separate keys** for development and production
5. **Store keys securely** using environment variables or secret managers

### 💰 Cost Management
1. **Monitor usage** regularly at: [https://platform.openai.com/usage](https://platform.openai.com/usage)
2. **Set spending limits** in your OpenAI account settings
3. **Use caching** to reduce redundant API calls
4. **Choose appropriate models** (GPT-3.5 is cheaper than GPT-4)
5. **Implement rate limiting** to prevent unexpected costs

### 📊 Model Selection

**Current Model: `gpt-3.5-turbo`** ✅

This is configured in `backend/openai_helper.py` at multiple locations:
- Line 73: `test_connection()` function
- Line 139: `get_completion()` function
- Line 268: Standalone `get_completion()` function

**Why GPT-3.5 Turbo?**
- ✅ Fast response times (< 2 seconds)
- ✅ Cost-effective ($0.0015 per 1K tokens)
- ✅ Perfect for document processing tasks
- ✅ Sufficient for summarization, Q&A, and text analysis

**Alternative Models:**
- `gpt-4` - Higher quality, slower, more expensive
- `gpt-4-turbo` - Faster GPT-4 with larger context window
- `gpt-3.5-turbo-16k` - Extended context for longer documents

To change the model, edit the `model` parameter in `backend/openai_helper.py`:
```python
model="gpt-3.5-turbo"  # Change this to your desired model
```

---

## API Reference

### Available Functions in `backend/openai_helper.py`

#### 1. `load_api_key()`
Loads and validates the API key from `.env` file.

**Returns**: `bool` - True if successful, False otherwise

**Example**:
```python
from backend.openai_helper import OpenAIHelper

helper = OpenAIHelper()
# API key is automatically loaded during initialization
```

#### 2. `test_connection()`
Tests the API connection by sending a simple prompt.

**Returns**: `dict` - Contains success status, response, model, and token usage

**Example**:
```python
result = helper.test_connection()
if result["success"]:
    print(f"Model: {result['model']}")
    print(f"Response: {result['response']}")
```

#### 3. `get_completion()`
Sends a prompt to OpenAI and returns the response.

**Parameters**:
- `prompt` (str): The user's question or instruction
- `system_message` (str): System context for the AI
- `model` (str): OpenAI model to use (default: "gpt-3.5-turbo")
- `temperature` (float): Creativity level (0.0-1.0, default: 0.7)
- `max_tokens` (int): Maximum response length (default: 500)

**Returns**: `dict` - Contains success status, response, and metadata

**Example**:
```python
result = helper.get_completion(
    prompt="Summarize this text: [your text here]",
    system_message="You are a helpful assistant for document processing.",
    temperature=0.5
)

if result["success"]:
    print(result["response"])
```

---

## Pricing Information (as of 2026)

### GPT-3.5 Turbo Pricing
- **Input**: $0.0015 per 1K tokens
- **Output**: $0.002 per 1K tokens

**Example Cost Calculation**:
- 1,000 words ≈ 750 tokens
- Processing 100 documents (1,000 words each):
  - Input: 75,000 tokens × $0.0015 = $0.11
  - Output: 25,000 tokens × $0.002 = $0.05
  - **Total**: ~$0.16

### Free Tier
- New accounts: **$5 in free credits**
- Valid for: **3 months**
- Enough for: ~2,500,000 tokens with GPT-3.5

---

## Additional Resources

### Official Documentation
- **OpenAI API Docs**: [https://platform.openai.com/docs](https://platform.openai.com/docs)
- **API Reference**: [https://platform.openai.com/docs/api-reference](https://platform.openai.com/docs/api-reference)
- **Pricing**: [https://openai.com/pricing](https://openai.com/pricing)
- **Rate Limits**: [https://platform.openai.com/docs/guides/rate-limits](https://platform.openai.com/docs/guides/rate-limits)

### Account Management
- **Usage Dashboard**: [https://platform.openai.com/usage](https://platform.openai.com/usage)
- **API Keys**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Billing**: [https://platform.openai.com/account/billing](https://platform.openai.com/account/billing)
- **Organization Settings**: [https://platform.openai.com/account/organization](https://platform.openai.com/account/organization)

### Support
- **Community Forum**: [https://community.openai.com](https://community.openai.com)
- **Help Center**: [https://help.openai.com](https://help.openai.com)
- **Status Page**: [https://status.openai.com](https://status.openai.com)

---

## Summary Checklist

Before proceeding with SmartDocs AI development, ensure:

- [ ] ✅ OpenAI account created and verified
- [ ] ✅ API key generated and copied
- [ ] ✅ `.env` file created in project root
- [ ] ✅ API key added to `.env` file
- [ ] ✅ `.env` file is in `.gitignore`
- [ ] ✅ Test script executed successfully
- [ ] ✅ API connection confirmed working
- [ ] ✅ Billing information added (if needed)
- [ ] ✅ Usage limits understood
- [ ] ✅ Model selection appropriate for use case

---

**🎉 Congratulations!** Your OpenAI API is now configured and ready for SmartDocs AI!

For questions or issues, refer to the [Troubleshooting](#troubleshooting) section or consult the [OpenAI Documentation](https://platform.openai.com/docs).

---

**Last Updated**: January 11, 2026  
**SmartDocs AI Version**: 1.0  
**OpenAI SDK Version**: 2.14.0
