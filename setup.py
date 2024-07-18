import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llmmaster",
    version="0.1.6",
    author="Daisuke Yamaguchi",
    author_email="daicom0204@gmail.com",
    description="A unified interface for interacting with multiple LLMs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Habatakurikei/llmmaster",
    packages=setuptools.find_packages(include=['llmmaster', 'llmmaster.*']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.25.9",
        "google-generativeai>=0.7.2",
        "groq>=0.5.0",
        "openai>=1.30.1",
        "pillow>=9.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=6.0",
        ],
    },
)
