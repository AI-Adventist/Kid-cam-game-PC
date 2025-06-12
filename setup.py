#!/usr/bin/env python3
"""
Setup script for Kid Cam Game PC
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="kid-cam-game-pc",
    version="1.0.0",
    author="AI-Adventist",
    description="A fun, interactive camera-based game designed for kids",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AI-Adventist/Kid-cam-game-PC",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Video :: Capture",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "kid-cam-game=main:main",
        ],
    },
    keywords="game kids camera opencv pygame computer-vision interactive",
    project_urls={
        "Bug Reports": "https://github.com/AI-Adventist/Kid-cam-game-PC/issues",
        "Source": "https://github.com/AI-Adventist/Kid-cam-game-PC",
    },
)
