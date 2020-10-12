# -*- coding: utf-8 -*-

import pathlib

from setuptools import setup, find_packages


ROOT_DIR = pathlib.Path(__file__).parent.resolve()

setup(
    name="authenticator",
    version="0.1.dev0",
    author="Julien Chaumont",
    author_email="authenticator@julienc.io",
    description="2FA code manager",
    long_description=(ROOT_DIR / "README.md").read_text(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/julienc91/authenticator/",
    packages=find_packages(),
    install_requires=(ROOT_DIR / "requirements.txt").read_text().splitlines(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
