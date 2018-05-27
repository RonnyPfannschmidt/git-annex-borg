import pkg_resources
from setuptools import setup

pkg_resources.require("setuptools>=39")

setup(setup_requires=["setuptools_scm"], use_scm_version=True)
