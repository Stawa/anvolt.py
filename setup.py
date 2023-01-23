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

install_requires = ""
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

extras_require = {"cli": ["click>=8.1.0", "tabulate>=0.9.0"]}

setup(
    name="anvolt.py",
    version=version,
    author="Stawa",
    description="Advanced tool with API integration and additional features",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points="""
    [console_scripts]
    anvolt=anvolt.cli:main
    """,
    url="https://anvolt.vercel.app/api/",
    project_urls={
        "Source": "https://github.com/Stawa/anvolt.py",
        "Tracker": "https://github.com/Stawa/anvolt.py/issues",
        "Changelog": "https://github.com/Stawa/anvolt.py/blob/main/CHANGELOG.md",
    },
    keywords=[
        "api",
        "anime",
        "games",
        "roleplay",
        "images",
        "trivia",
        "discord",
        "webhooks",
        "twitch",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Typing :: Typed",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
)
