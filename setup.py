from setuptools import setup, find_packages

setup(
    name="bomberman-game",
    version="1.0.0",
    description="A Python implementation of the classic Bomberman game",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "bomberman=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
