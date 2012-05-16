from setuptools import setup, find_packages
import os

setup(
    name = "parker",
    version = "0.0.1",
    packages = ['parker',],
    author = "Cox Media Group",
    author_email = "opensource@coxinc.com",
    description = "Simple realtime publishing for django via browsermq",
    license = "MIT",
    url = "https://github.com/coxmediagroup/parker",
    install_requires = ['kombu',],
)

