# API Setup Guide for RizzScript

This guide provides detailed instructions for obtaining and configuring the API keys required by RizzScript.

## AssemblyAI API Setup (Required)

AssemblyAI provides the core speech-to-text and speaker diarization capabilities for RizzScript.

### Step 1: Create an AssemblyAI Account

1. Visit [AssemblyAI's website](https://www.assemblyai.com/)
2. Click "Sign Up" or "Get Started"
3. Create your account using email or GitHub authentication
4. Verify your email address if required

### Step 2: Obtain Your API Key

1. Log in to your AssemblyAI dashboard
2. Navigate to the "API Keys" section (usually in account settings)
3. Copy your API key (it starts with a long alphanumeric string)
4. **Important**: Keep this key secure and never share it publicly

### Step 3: Understanding AssemblyAI Pricing

- **Free Tier**: Includes limited transcription minutes per month
- **Pay-as-you-go**: Charged per audio minute transcribed
- **Enterprise Plans**: Available for high-volume usage

**Pricing Information**: [AssemblyAI Pricing](https://www.assemblyai.com/pricing)

### Step 4: Configure in RizzScript

1. Open RizzScript
2. Go to `File > Settings`
3. Paste your API key in the "AssemblyAI API Key" field
4. Click "OK" to save

## OpenAI API Setup (Optional but Recommended)

OpenAI powers the intelligent speaker identification feature in RizzScript.

### Step 1: Create an OpenAI Account

1. Visit [OpenAI's platform](https://platform.openai.com/)
2. Click "Sign up" to create an account
3. Verify your email and complete account setup
4. Add a payment method (required for API access)

### Step 2: Obtain Your API Key

1. Log in to your OpenAI dashboard
2. Navigate to "API Keys" in the left sidebar
3. Click "Create new secret key"
4. Give your key a descriptive name (e.g., "RizzScript")
5. Copy the generated key (starts with `sk-`)
6. **Critical**: Store this key securely - you won't be able to see it again

### Step 3: Understanding OpenAI Pricing

- **Usage-based Billing**: Pay per token (words/characters processed)
- **Model Costs**: Different models have different pricing
- **RizzScript Usage**: Uses GPT-4 for speaker analysis (moderate cost)

**Estimated Costs**:
- Small conversation (5-10 minutes): $0.01-0.05
- Medium conversation (30-60 minutes): $0.05-0.25
- Large conversation (2+ hours): $0.25-1.00+

**Pricing Details**: [OpenAI Pricing](https://openai.com/pricing)

### Step 4: Set Usage Limits (Recommended)

1. In your OpenAI dashboard, go to "Usage limits"
2. Set a monthly spending limit to control costs
3. Set up email notifications for usage alerts

### Step 5: Configure in RizzScript

1. Open RizzScript
2. Go to `File > Settings`
3. Paste your API key in the "OpenAI API Key" field
4. Click "OK" to save

## Security Best Practices

### API Key Security

1. **Never commit API keys to version control**
2. **Don't share keys in screenshots or public forums**
3. **Rotate keys periodically** (monthly or quarterly)
4. **Use environment variables** for production deployments
5. **Monitor usage regularly** for unexpected activity

### RizzScript Configuration

The `config.json` file stores your API keys locally:
```json
{
    "assemblyai_api_key": "your_assemblyai_key_here",
    "openai_api_key": "your_openai_key_here"
}
```

**Important**: This file is automatically added to `.gitignore` to prevent accidental commits.

## Troubleshooting API Issues

### AssemblyAI Common Issues

#### Invalid API Key Error
- **Symptom**: "Invalid API key" or authentication errors
- **Solutions**:
  - Verify key is copied correctly (no extra spaces)
  - Check if key has been revoked or expired
  - Ensure account is in good standing

#### Quota Exceeded
- **Symptom**: "Quota exceeded" or similar rate limit errors
- **Solutions**:
  - Check your AssemblyAI dashboard for usage limits
  - Upgrade to a higher tier if needed
  - Wait for quota reset (usually monthly)

#### Unsupported Audio Format
- **Symptom**: Transcription fails with format errors
- **Solutions**:
  - Convert audio to supported format (MP3, WAV, OGG)
  - Check file isn't corrupted
  - Ensure file size is within limits

### OpenAI Common Issues

#### Insufficient Credits
- **Symptom**: "Insufficient quota" or billing errors
- **Solutions**:
  - Add funds to your OpenAI account
  - Check billing settings and payment methods
  - Review usage history for unexpected charges

#### Rate Limit Exceeded
- **Symptom**: "Rate limit exceeded" errors
- **Solutions**:
  - Wait a few minutes before retrying
  - Consider upgrading to higher rate limits
  - Use speaker mapping less frequently

#### Model Access Issues
- **Symptom**: Model not available or access denied
- **Solutions**:
  - Ensure your account has access to GPT-4
  - Check OpenAI's service status
  - Try again later if there are temporary outages

## Alternative Configurations

### Using Only AssemblyAI (No OpenAI)

If you prefer not to use OpenAI:
1. Leave the OpenAI API key field empty
2. Use manual speaker mapping instead of auto-population
3. All core transcription features will still work perfectly

### Environment Variables (Advanced)

For automated deployments, you can set environment variables:
```bash
export ASSEMBLYAI_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"
```

Modify the application to read from environment variables if preferred.

## Support and Resources

### AssemblyAI Resources
- [Documentation](https://www.assemblyai.com/docs/)
- [API Reference](https://www.assemblyai.com/docs/api-reference)
- [Support](https://www.assemblyai.com/contact)

### OpenAI Resources
- [Documentation](https://platform.openai.com/docs)
- [API Reference](https://platform.openai.com/docs/api-reference)
- [Community Forum](https://community.openai.com/)

### Need Help?

If you encounter issues not covered in this guide:
1. Check the main [README.md](README.md) troubleshooting section
2. Search existing GitHub issues
3. Create a new issue with detailed error information
4. Contact the developer:
   - **Mark Rizzn Hopkins**: guesswho@rizzn.com
   - **Twitter**: [@rizzn](https://twitter.com/rizzn)
   - **GitHub**: [@actuallyrizzn](https://github.com/actuallyrizzn)

---

**Important**: API services and pricing may change. Always refer to the official provider documentation for the most current information.