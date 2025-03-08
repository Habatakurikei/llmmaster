import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="llmmaster",
    version="1.0.0",
    author="Daisuke Yamaguchi",
    author_email="daicom0204@gmail.com",
    description="A unified interface for interacting with multiple LLMs and generative AIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/llmmaster/",
    project_urls={
        "Homepage": "https://habatakurikei.com/",
        "GitHub": "https://github.com/Habatakurikei/llmmaster",
    },
    packages=setuptools.find_packages(include=["llmmaster", "llmmaster.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.32.3",
        "requests-toolbelt>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "flake8>=7.1.1",
            "setuptools>=75.8.0",
            "twine>=6.1.0",
        ],
    },
)
