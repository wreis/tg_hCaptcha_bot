"""The setup and build script for the tg_hcaptcha_bot library."""

import os
from setuptools import setup, find_packages

def requirements():
    """Build the requirements list for this project"""

    with open('requirements.txt') as requirements:
        return [ install.strip() for install in requirements ]

setup(
    name="tg_hcaptcha_bot",
    version="0.1",
    packages=find_packages(),

    install_requires=requirements(),

    include_package_data=True,

    author="Wallace Reis",
    author_email="wallace@reis.me",
    description="Bot for Telegram groups using hCaptcha",
    url="https://github.com/wreis/tg_hCaptcha_bot",
)
