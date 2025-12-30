#!/usr/bin/env python3
"""
Setup Verification Script
Checks that all dependencies and required components are properly installed
"""

import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_header(text):
    """Print a header"""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}{text.center(60)}{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")

def print_check(name, status, message=""):
    """Print a check result"""
    status_symbol = f"{Colors.GREEN}✓{Colors.NC}" if status else f"{Colors.RED}✗{Colors.NC}"
    print(f"{status_symbol} {name:<40} {message}")
    return status

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return print_check(
        "Python version (>=3.8)",
        is_valid,
        f"v{version_str}"
    )

def check_module(module_name, package_name=None):
    """Check if a Python module is installed"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        return print_check(f"Module: {package_name}", True, "Installed")
    except ImportError:
        return print_check(f"Module: {package_name}", False, "Not found")

def check_command(command, name=None):
    """Check if a system command is available"""
    if name is None:
        name = command
    
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        version = result.stdout.split('\n')[0] if result.stdout else "Available"
        return print_check(f"Command: {name}", result.returncode == 0, version)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return print_check(f"Command: {name}", False, "Not found")

def check_directory(path, name=None):
    """Check if a directory exists"""
    if name is None:
        name = path
    
    exists = Path(path).is_dir()
    return print_check(f"Directory: {name}", exists, "Exists" if exists else "Missing")

def check_file(path, name=None):
    """Check if a file exists"""
    if name is None:
        name = path
    
    exists = Path(path).is_file()
    return print_check(f"File: {name}", exists, "Exists" if exists else "Missing")

def check_env_file():
    """Check if .env file exists"""
    env_exists = Path('.env').is_file()
    env_example_exists = Path('.env.example').is_file()
    
    if env_exists:
        return print_check(".env configuration", True, "Found")
    elif env_example_exists:
        return print_check(".env configuration", False, ".env.example found (copy to .env)")
    else:
        return print_check(".env configuration", False, "Not found")

def main():
    """Run all verification checks"""
    print_header("Epstein Files Hub - Setup Verification")
    
    all_passed = True
    
    # Core Python checks
    print(f"\n{Colors.YELLOW}Core Requirements:{Colors.NC}")
    all_passed &= check_python_version()
    all_passed &= check_command("pip3", "pip3")
    all_passed &= check_command("git", "git")
    
    # Python dependencies
    print(f"\n{Colors.YELLOW}Python Dependencies:{Colors.NC}")
    all_passed &= check_module("requests")
    all_passed &= check_module("pypdf", "pypdf")
    all_passed &= check_module("PIL", "Pillow")
    all_passed &= check_module("pytesseract")
    all_passed &= check_module("pdf2image")
    all_passed &= check_module("feedparser")
    
    # Optional system commands
    print(f"\n{Colors.YELLOW}Optional System Commands:{Colors.NC}")
    tesseract = check_command("tesseract", "tesseract (OCR)")
    check_command("docker", "docker")
    check_command("docker-compose", "docker-compose")
    
    # Required directories
    print(f"\n{Colors.YELLOW}Required Directories:{Colors.NC}")
    all_passed &= check_directory("data")
    all_passed &= check_directory("scripts")
    all_passed &= check_directory("web")
    all_passed &= check_directory("bots")
    all_passed &= check_directory("docs")
    
    # Check if directories are created
    print(f"\n{Colors.YELLOW}Data Directories:{Colors.NC}")
    check_directory("data/public_files", "data/public_files")
    check_directory("data/processed", "data/processed")
    check_directory("data/wikipedia", "data/wikipedia")
    check_directory("logs", "logs")
    check_directory("cache", "cache")
    check_directory("tmp", "tmp")
    
    # Required files
    print(f"\n{Colors.YELLOW}Required Files:{Colors.NC}")
    all_passed &= check_file("requirements.txt")
    all_passed &= check_file("setup.py")
    all_passed &= check_file("setup.sh")
    all_passed &= check_file("Dockerfile")
    all_passed &= check_file("docker-compose.yml")
    all_passed &= check_file("Makefile")
    
    # Configuration files
    print(f"\n{Colors.YELLOW}Configuration Files:{Colors.NC}")
    check_env_file()
    check_file(".env.example")
    check_file(".gitignore")
    check_file(".dockerignore")
    
    # Python scripts
    print(f"\n{Colors.YELLOW}Python Scripts:{Colors.NC}")
    all_passed &= check_file("scripts/fetch-public-files.py")
    all_passed &= check_file("scripts/fetch-wikipedia-data.py")
    all_passed &= check_file("scripts/generate-search-index.py")
    all_passed &= check_file("scripts/process-pdfs.py")
    all_passed &= check_file("scripts/safe-source-expander.py")
    
    # Virtual environment check
    print(f"\n{Colors.YELLOW}Virtual Environment:{Colors.NC}")
    venv_exists = Path('.venv').is_dir()
    if venv_exists:
        print_check("Virtual environment", True, ".venv found")
    else:
        print_check("Virtual environment", False, "Run ./setup.sh to create")
    
    # Summary
    print_header("Verification Summary")
    
    if all_passed:
        print(f"{Colors.GREEN}✓ All required components are installed!{Colors.NC}")
        print(f"\n{Colors.GREEN}You're ready to start using the Epstein Files Hub.{Colors.NC}\n")
        
        print(f"Quick start commands:")
        print(f"  make fetch-public-files  # Fetch FBI Vault files")
        print(f"  make fetch-wikipedia     # Fetch Wikipedia data")
        print(f"  make generate-index      # Generate search index")
        print(f"  make serve               # Start local web server")
        print(f"\nSee 'make help' for all available commands.\n")
        return 0
    else:
        print(f"{Colors.RED}✗ Some required components are missing.{Colors.NC}")
        print(f"\n{Colors.YELLOW}Recommended actions:{Colors.NC}")
        print(f"  1. Run ./setup.sh to set up the environment")
        print(f"  2. Install missing Python packages: pip install -r requirements.txt")
        print(f"  3. Check SETUP_GUIDE.md for detailed instructions")
        
        if not tesseract:
            print(f"\n{Colors.YELLOW}Note: Tesseract OCR is optional but recommended for PDF processing.{Colors.NC}")
            print(f"  Install: sudo apt-get install tesseract-ocr (Linux)")
            print(f"  Install: brew install tesseract (Mac)")
        
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
