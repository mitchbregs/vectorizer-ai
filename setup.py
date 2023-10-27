from setuptools import setup, find_packages

setup(
    name="vectorizer_ai",
    version="0.0.1",
    python_requires=">3.6",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Mitchell Bregman",
    author_email="mitch@mitchbregs.com",
    description="Python SDK for vectorizer.ai",
    keywords="vectorizer.ai svg vectorize image",
    url="https://github.com/mitchbregs/vectorizer-ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
