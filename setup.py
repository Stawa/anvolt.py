from setuptools import setup, find_packages
import re

README = ""
with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

version = ""
with open("anvolt/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

setup(
    name="anvolt.py",
    version=version,
    author="Stawa",
    description="Advanced tool with API integration and additional features",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    url="https://github.com/Stawa/anvolt.py",
    project_urls={
        "Source": "https://github.com/Stawa/anvolt.py",
        "Tracker": "https://github.com/Stawa/anvolt.py/issues",
        "Changelog": "https://github.com/Stawa/anvolt.py/blob/main/CHANGELOG.md",
    },
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Typing :: Typed",
        "Intended Audience :: Developers",
    ],
)
