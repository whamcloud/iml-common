# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

excludes = ["*tests*"]

setup(
    name="iml-common",
    version="1.5.0",
    author="Whamcloud",
    author_email="iml@whamcloud.com",
    url="https://pypi.python.org/pypi/iml-common",
    packages=find_packages(exclude=excludes),
    license="MIT",
    test_suite="tests",
    description="Common library used by multiple IML components",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="IML lustre high-availability",
)
