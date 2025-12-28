# Setup Guide - Epstein Files Hub

## 📋 Overview

This guide provides comprehensive instructions for setting up the Epstein Files Hub development environment. The project includes Python scripts, Docker containerization, and automated workflows for managing and indexing Epstein-related documentation.

---

## 🎯 Quick Start (5 minutes)

```bash
# 1. Clone the repository (if not already done)
git clone https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory

# 2. Run the automated setup
./setup.sh

# 3. Verify installation
python verify-setup.py

# 4. Start using the tools
make help
```

---

## 📦 Prerequisites

### Required Software

- **Python 3.8+** - Core scripting language
- **pip** - Python package manager
- **Git** - Version control

### Optional Software

- **Docker & Docker Compose** - For containerized deployment
- **Tesseract OCR** - For PDF text extraction from scanned documents
- **Make** - For using the Makefile commands (pre-installed on most Unix systems)

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 5GB minimum for full data processing
- **Network**: Internet connection for fetching public files

---

## 🔧 Installation Methods

### Method 1: Automated Setup (Recommended)

The automated setup script handles everything for you:

```bash
./setup.sh
```

This script will:
1. ✅ Check Python version (3.8+)
2. ✅ Create Python virtual environment (`.venv`)
3. ✅ Install all dependencies from `requirements.txt`
4. ✅ Create required directories (`data/`, `logs/`, `cache/`, `tmp/`)
5. ✅ Set up `.env` file from template
6. ✅ Check for optional dependencies (Tesseract)

### Method 2: Manual Setup

If you prefer manual control:

#### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate  # Windows
```

#### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Optional: Install development dependencies
pip install pytest pytest-cov ipython black flake8 mypy
```

#### Step 3: Create Required Directories

```bash
mkdir -p data/public_files/fbi_vault
mkdir -p data/wikipedia
mkdir -p data/processed/{text,metadata,indexed}
mkdir -p logs cache tmp
```

#### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor
```

#### Step 5: Install System Dependencies (Optional)

For OCR support:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng poppler-utils

# macOS (with Homebrew)
brew install tesseract poppler

# Verify installation
tesseract --version
```

### Method 3: Docker Setup

For containerized deployment:

```bash
# Build Docker images
docker-compose build

# Or use Make
make docker-build

# Start the development container
docker-compose up -d app

# Or use Make
make docker-up

# Access the container
docker-compose exec app /bin/bash
```

---

## 📁 Directory Structure

After setup, your project structure will look like this:

```
Hub_of_Epstein_Files_Directory/
├── .venv/                      # Python virtual environment
├── .env                        # Environment configuration (create from .env.example)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── .dockerignore              # Docker ignore rules
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker services configuration
├── Makefile                   # Common commands
├── setup.sh                   # Automated setup script
├── setup.py                   # Python package configuration
├── verify-setup.py            # Installation verification
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── QUICK_START.md            # Quick start guide
├── SETUP_GUIDE.md            # This file
├── CONTRIBUTING.md           # Contribution guidelines
│
├── bots/                      # AI agent infrastructure
│   ├── pdf-analysis-bot/
│   ├── search-bot/
│   └── ... (26 total agents)
│
├── data/                      # Data storage
│   ├── public_files/         # Downloaded public files
│   │   └── fbi_vault/        # FBI Vault PDFs
│   ├── wikipedia/            # Wikipedia data
│   └── processed/            # Processed data
│       ├── text/             # Extracted text
│       ├── metadata/         # Document metadata
│       └── indexed/          # Search indices
│
├── docs/                      # Documentation
│   ├── FREE_TIER_SETUP.md
│   ├── Bot-Usage-Guide.md
│   └── ... (various guides)
│
├── scripts/                   # Python scripts
│   ├── fetch-public-files.py
│   ├── fetch-wikipedia-data.py
│   ├── generate-search-index.py
│   ├── process-pdfs.py
│   └── safe-source-expander.py
│
├── web/                       # Web interface
│   ├── index.html
│   ├── search.html
│   ├── css/
│   ├── js/
│   └── ... (8 pages total)
│
├── logs/                      # Application logs
├── cache/                     # Temporary cache
└── tmp/                       # Temporary files
```

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# GitHub OAuth (for staff portal)
GITHUB_OAUTH_CLIENT_ID=your_client_id
GITHUB_OAUTH_CLIENT_SECRET=your_client_secret

# Application settings
ENVIRONMENT=development
LOG_LEVEL=INFO

# Processing settings
OCR_ENABLED=true
MAX_PDF_SIZE_MB=100

# Source monitoring
FBI_VAULT_ENABLED=true
WIKIPEDIA_ENABLED=true
SOURCE_DISCOVERY_ENABLED=true
```

See `.env.example` for all available options.

---

## 🚀 Usage

### Using Make Commands (Recommended)

The Makefile provides convenient commands:

```bash
# Show all available commands
make help

# Data processing
make fetch-public-files    # Fetch FBI Vault PDFs
make fetch-wikipedia       # Fetch Wikipedia data
make process-pdfs          # Process PDFs with OCR
make generate-index        # Generate search index
make fetch-all             # Run all data operations

# Development
make serve                 # Start local web server (port 8080)
make format                # Format Python code
make lint                  # Lint Python code
make test                  # Run tests

# Docker operations
make docker-build          # Build Docker images
make docker-up             # Start containers
make docker-down           # Stop containers
make docker-shell          # Open shell in container

# Cleanup
make clean                 # Clean temporary files
make clean-data            # Clean processed data (WARNING)
make clean-all             # Clean everything (WARNING)

# Information
make info                  # Show project information
make status                # Show system status
```

### Running Scripts Directly

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run individual scripts
python scripts/fetch-public-files.py
python scripts/fetch-wikipedia-data.py
python scripts/generate-search-index.py
python scripts/process-pdfs.py
python scripts/safe-source-expander.py

# With custom options
python scripts/process-pdfs.py --input-dir data/custom --output-dir data/output
```

### Using Docker

```bash
# Run specific services
docker-compose run --rm fetch-public-files
docker-compose run --rm process-pdfs
docker-compose run --rm generate-search-index

# Start web server
docker-compose --profile web up web
# Access at http://localhost:8080

# View logs
docker-compose logs -f app

# Execute commands in running container
docker-compose exec app python scripts/fetch-public-files.py
```

---

## ✅ Verification

### Verify Installation

Run the verification script to check all dependencies:

```bash
python verify-setup.py
```

This checks:
- ✅ Python version
- ✅ Required modules
- ✅ Optional system commands
- ✅ Directory structure
- ✅ Configuration files
- ✅ Python scripts

### Test Data Processing

```bash
# Test fetch (without downloading large files)
python scripts/fetch-public-files.py --dry-run

# Test search index generation
python scripts/generate-search-index.py

# Start local web server to test interface
make serve
# Visit http://localhost:8080
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Python Version Too Old

**Error**: `Python 3.8+ required`

**Solution**:
```bash
# Check version
python3 --version

# Install Python 3.11 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# Use specific version
python3.11 -m venv .venv
```

#### 2. Permission Denied

**Error**: `Permission denied: ./setup.sh`

**Solution**:
```bash
chmod +x setup.sh verify-setup.py
./setup.sh
```

#### 3. Missing Tesseract

**Error**: `tesseract not found`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

#### 4. Docker Build Fails

**Error**: `failed to solve with frontend dockerfile.v0`

**Solution**:
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### 5. Import Errors

**Error**: `ModuleNotFoundError: No module named 'requests'`

**Solution**:
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 6. Out of Disk Space

**Error**: `No space left on device`

**Solution**:
```bash
# Check disk usage
df -h

# Clean up
make clean
docker system prune -a --volumes

# Remove large data files
rm -rf data/public_files/*  # WARNING: destructive
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use virtual environment** - Isolates dependencies
3. **Keep dependencies updated** - Regular `pip install --upgrade`
4. **Review Docker images** - Use official base images
5. **Limit file permissions** - Use non-root Docker user
6. **Validate downloads** - Check SHA-256 hashes

---

## 📊 Performance Optimization

### For Large Datasets

```bash
# Increase cache size
export CACHE_SIZE=1000

# Use multiprocessing
python scripts/process-pdfs.py --workers 4

# Optimize Docker
docker-compose up -d --scale process-pdfs=3
```

### For Low Memory Systems

```bash
# Process in batches
python scripts/process-pdfs.py --batch-size 10

# Reduce OCR quality
export OCR_DPI=150  # Default is 300
```

---

## 🔄 Updating

### Update Dependencies

```bash
# Pull latest code
git pull origin main

# Update Python packages
pip install --upgrade -r requirements.txt

# Rebuild Docker images
make docker-build
```

### Migrate Data

```bash
# Backup existing data
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Run migrations (if any)
python scripts/migrate-data.py

# Regenerate search index
make generate-index
```

---

## 🧪 Development Workflow

### 1. Initial Setup

```bash
git clone https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory.git
cd Hub_of_Epstein_Files_Directory
./setup.sh
```

### 2. Daily Development

```bash
# Activate environment
source .venv/bin/activate

# Make changes to code
# ...

# Format and lint
make format
make lint

# Test changes
make test

# Run scripts
python scripts/your-script.py
```

### 3. Testing Changes

```bash
# Unit tests
pytest tests/

# Integration tests
make fetch-public-files
make generate-index
make serve
```

### 4. Committing Changes

```bash
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push origin your-branch
```

---

## 📚 Additional Resources

- **Project README**: [README.md](README.md)
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Free Tier Setup**: [docs/FREE_TIER_SETUP.md](docs/FREE_TIER_SETUP.md)
- **Bot Usage Guide**: [docs/Bot-Usage-Guide.md](docs/Bot-Usage-Guide.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💬 Support

### Getting Help

1. **Check this guide** - Most issues are covered here
2. **Run verification** - `python verify-setup.py`
3. **Check logs** - `cat logs/latest.log`
4. **GitHub Issues** - Report bugs or ask questions
5. **GitHub Discussions** - Community support

### Reporting Issues

When reporting issues, include:
- Output of `python verify-setup.py`
- Output of `make info`
- Relevant log files from `logs/`
- Steps to reproduce the issue
- Expected vs actual behavior

---

## ✅ Post-Setup Checklist

After completing setup, verify:

- [ ] Python virtual environment created (`.venv/`)
- [ ] All dependencies installed (`verify-setup.py` passes)
- [ ] Environment configured (`.env` exists)
- [ ] Required directories created (`data/`, `logs/`, etc.)
- [ ] Can run scripts (`python scripts/fetch-public-files.py --help`)
- [ ] Web server works (`make serve` → http://localhost:8080)
- [ ] Docker builds successfully (`make docker-build`)
- [ ] Tests pass (`make test`)

---

**Last Updated**: December 28, 2024  
**Version**: 1.0.0  
**Maintainer**: IAmSoThirsty

**Ready to start?** Run `./setup.sh` and then `make help` to see available commands!
