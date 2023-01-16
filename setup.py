from setuptools import setup, find_packages

README = ""
with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="anvolt.py",
    version="0.1.1",
    author="Stawa",
    description="Test",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    url="https://github.com/Stawa/anvolt.py",
    project_urls={
        "Documentation": "",
        "Source": "https://github.com/Stawa/anvolt.py",
        "Tracker": "https://github.com/Stawa/anvolt.py/issues",
        "Changelog": "https://github.com/Stawa/anvolt.py/blob/main/CHANGELOG.md",
    },
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
)
