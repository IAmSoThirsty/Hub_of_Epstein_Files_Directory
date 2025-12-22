# Bot Infrastructure Setup Guide

This guide walks you through setting up the bot infrastructure for the Epstein Files Hub.

## Prerequisites

### Required Accounts
- GitHub account
- Azure subscription (for AI services)
- Python 3.9 or higher

### Required Tools
```bash
# Install Python and pip
python --version  # Should be 3.9+
pip --version

# Install Git
git --version

# Install Azure CLI (optional, for Azure services)
# Download installation script
curl -sL https://aka.ms/InstallAzureCLIDeb -o /tmp/install-azure-cli.sh
# Review the script before executing
less /tmp/install-azure-cli.sh
# Execute if safe
sudo bash /tmp/install-azure-cli.sh

# Or install via package manager (recommended)
# Ubuntu/Debian:
# sudo apt-get install azure-cli
```

---

## Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory

# Navigate to bots directory
cd bots
```

---

## Step 2: Install Dependencies

### Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
python -c "import PyPDF2, requests; print('✅ Dependencies installed')"
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    python3-pip \
    python3-dev
```

**macOS:**
```bash
brew install tesseract poppler python
```

**Windows:**
1. Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Add to PATH
3. Install poppler from: https://github.com/oschwartz10612/poppler-windows

---

## Step 3: Configure Azure Services (Optional)

If using Azure AI services:

### Create Azure Resources
```bash
# Login to Azure
az login

# Create resource group
az group create --name epstein-files-rg --location eastus

# Create Cognitive Services account
az cognitiveservices account create \
    --name epstein-files-cognitive \
    --resource-group epstein-files-rg \
    --kind CognitiveServices \
    --sku S0 \
    --location eastus
```

### Get API Keys
```bash
# Get keys
az cognitiveservices account keys list \
    --name epstein-files-cognitive \
    --resource-group epstein-files-rg
```

---

## Step 4: Environment Configuration

### Create .env File
```bash
# Create .env file in bots/ directory
cat > .env << EOF
# Azure Cognitive Services
AZURE_COGNITIVE_KEY=your_key_here
AZURE_COGNITIVE_ENDPOINT=https://your_endpoint.cognitiveservices.azure.com/

# Azure Search
AZURE_SEARCH_KEY=your_search_key_here
AZURE_SEARCH_ENDPOINT=https://your_search.search.windows.net

# GitHub
GITHUB_TOKEN=your_github_token_here

# Bot Configuration
BOT_LOG_LEVEL=INFO
BOT_MAX_WORKERS=4
EOF
```

### Load Environment Variables
```bash
# Recommended: Use python-dotenv
pip install python-dotenv

# Or manually load (safer than export $(cat .env | xargs))
set -a
source .env
set +a
```

---

## Step 5: Configure GitHub Actions

### Add Secrets to GitHub

1. Go to repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `AZURE_COGNITIVE_KEY`
   - `AZURE_COGNITIVE_ENDPOINT`
   - `AZURE_SEARCH_KEY`
   - `AZURE_SEARCH_ENDPOINT`

### Enable Workflows

1. Go to repository Actions tab
2. Enable workflows:
   - Bot Monitoring
   - PDF Analysis
   - Document Indexing
   - Search Index Updates

---

## Step 6: Test Bot Installation

### Test Individual Bots

```bash
# Test PDF Analysis Bot
python pdf-analysis-bot/analyze.py --help

# Test Search Bot (if configured)
# python search-bot/search.py --query "test"

# Test with sample document
python pdf-analysis-bot/analyze.py --file ../data/sample.pdf
```

### Run Bot Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest bots/ -v

# Run specific bot tests
pytest bots/pdf-analysis-bot/tests/ -v
```

---

## Step 7: Configure Bot Orchestration

### Create Orchestration Config

```bash
# Edit bots/config/orchestration.yml
cat > config/orchestration.yml << EOF
version: "1.0"

workflows:
  document_upload:
    - bot: pdf-analysis-bot
      timeout: 30
    - bot: indexing-bot
      timeout: 60
    - bot: entity-extraction-bot
      timeout: 45

  search_query:
    - bot: search-bot
      timeout: 10

schedule:
  daily:
    - bot: verification-bot
      time: "02:00"
    - bot: fact-checking-bot
      time: "03:00"
  
  weekly:
    - bot: summarization-bot
      day: "sunday"
      time: "04:00"
EOF
```

---

## Step 8: Verify Setup

### Run Setup Verification Script

```bash
# Create verification script
cat > verify-setup.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

checks = {
    "Python version": sys.version_info >= (3, 9),
    ".env file": os.path.exists('.env'),
    "PDF bot": os.path.exists('pdf-analysis-bot/analyze.py'),
    "Search bot": os.path.exists('search-bot/README.md'),
}

print("🔍 Verifying bot setup...\n")
all_pass = True
for check, status in checks.items():
    symbol = "✅" if status else "❌"
    print(f"{symbol} {check}")
    if not status:
        all_pass = False

if all_pass:
    print("\n✅ Setup complete!")
else:
    print("\n❌ Some checks failed. Review setup steps.")
    sys.exit(1)
EOF

python verify-setup.py
```

---

## Troubleshooting

### Common Issues

**Issue: Import errors**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Azure authentication fails**
```bash
# Solution: Re-login to Azure
az logout
az login
```

**Issue: Environment variables not loading**
```bash
# Solution: Check .env file
cat .env
# Reload environment
export $(cat .env | xargs)
```

**Issue: Bot tests fail**
```bash
# Solution: Check test configuration
pytest bots/ -v --tb=short
```

---

## Next Steps

1. Read [DEVELOPMENT.md](DEVELOPMENT.md) for bot development guidelines
2. Review individual bot README files
3. Configure GitHub Actions workflows
4. Test bots with sample documents
5. Monitor bot performance

---

## Free Tier Alternative

If you want to avoid Azure costs, use the free tier setup:

- ✅ Client-side search with Lunr.js (no Azure Search needed)
- ✅ Local OCR with Tesseract (no Azure Document Intelligence)
- ✅ GitHub Actions for automation (2,000 minutes/month free)

See [../docs/FREE_TIER_SETUP.md](../docs/FREE_TIER_SETUP.md) for details.

---

## Support

- **Documentation:** Individual bot README files
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

*Last Updated: December 2024*
