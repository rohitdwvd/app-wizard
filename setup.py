from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="app-wizard",
    version="0.1.0",
    author="Rohit Dwivedi",
    author_email="rohit.dwivedi@guenstiger.de",
    description="A modular MCP server for identifying addresses from text using various AI providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitdwvd/app-wizard",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "app-wizard=src.main:main",
        ],
    },
)