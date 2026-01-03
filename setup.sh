#!/bin/bash
# Setup script for Epstein Files Hub development environment
# This script sets up Python virtual environment and installs all dependencies

set -e  # Exit on error

echo "================================================"
echo "Epstein Files Hub - Environment Setup"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Found pip3${NC}"

# Create virtual environment
echo ""
echo "Creating Python virtual environment (.venv)..."
if [ -d ".venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists. Removing...${NC}"
    rm -rf .venv
fi

python3 -m venv .venv
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo "Creating required directories..."
mkdir -p data/public_files/fbi_vault
mkdir -p data/wikipedia
mkdir -p data/processed/text
mkdir -p data/processed/metadata
mkdir -p data/processed/indexed
mkdir -p logs
mkdir -p cache
mkdir -p tmp
echo -e "${GREEN}✓ Directories created${NC}"

# Create .env file if it doesn't exist
echo ""
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env from .env.example${NC}"
        echo -e "${YELLOW}⚠ Please edit .env with your configuration${NC}"
    else
        echo -e "${YELLOW}⚠ .env.example not found. Skipping .env creation${NC}"
    fi
else
    echo -e "${YELLOW}⚠ .env already exists. Skipping${NC}"
fi

# Check for Tesseract (OCR)
echo ""
echo "Checking optional dependencies..."
if command -v tesseract &> /dev/null; then
    echo -e "${GREEN}✓ Tesseract OCR is installed${NC}"
else
    echo -e "${YELLOW}⚠ Tesseract OCR is not installed${NC}"
    echo "  Install with: sudo apt-get install tesseract-ocr (Linux)"
    echo "  or: brew install tesseract (Mac)"
fi

# Summary
echo ""
echo "================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "================================================"
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "To run scripts:"
echo "  python scripts/fetch-public-files.py"
echo "  python scripts/generate-search-index.py"
echo ""
echo "See SETUP_GUIDE.md for more information"
echo ""
