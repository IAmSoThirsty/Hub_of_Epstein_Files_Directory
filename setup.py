"""
Epstein Files Hub - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding='utf-8').splitlines()
requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="epstein-files-hub",
    version="1.0.0",
    description="Comprehensive directory and organizational hub for Epstein-related files and documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="IAmSoThirsty",
    author_email="",
    url="https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory",
    packages=find_packages(where='.', exclude=['tests', 'tests.*']),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Researchers",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="epstein files documentation search indexing",
    project_urls={
        "Bug Reports": "https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory/issues",
        "Source": "https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory",
        "Documentation": "https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory/blob/main/README.md",
    },
    entry_points={
        'console_scripts': [
            'fetch-public-files=scripts.fetch_public_files:main',
            'fetch-wikipedia=scripts.fetch_wikipedia_data:main',
            'generate-search-index=scripts.generate_search_index:main',
            'process-pdfs=scripts.process_pdfs:main',
            'safe-source-expander=scripts.safe_source_expander:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
