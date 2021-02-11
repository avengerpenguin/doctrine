from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="doctrine",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "doctrine/_version.py",
        "fallback_version": "0.0.0",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    url="https://github.com/avengerpenguin/doctrine",
    packages=["doctrine"],
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    install_requires=["invoke"],
    extras_require={
        "test": ["pytest", "pytest-watch", "pytest-pikachu"],
    },
)
