from setuptools import setup, find_packages

setup(
    name="semantic_analysis",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pandas>=2.0.0",
        "openpyxl>=3.0.0",
        "python-dotenv>=1.0.0",
    ],
    description="Semantic analysis project for word meanings using LLMs"
) 