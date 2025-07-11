from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cursor-devops-toolkit",
    version="0.1.0",
    author="Your Name",
    description="A toolkit to extend Cursor with Linear and GitHub capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cursor-devops-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.1.0",
        "python-dotenv>=1.0.0",
        "loguru>=0.7.0",
        "httpx>=0.27.0",
        "tenacity>=8.2.0",
        "PyGithub>=2.2.0",
    ],
    entry_points={
        "console_scripts": [
            "cursor-toolkit=src.main:cli",
            "ctk=src.main:cli",  # Short alias
        ],
    },
) 