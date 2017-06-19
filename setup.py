#!/usr/bin/env python
# Copyright (c) 2017 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.


from setuptools import setup, find_packages

excludes = ["*tests*"]

setup(
    name = 'iml-common',
    version = '1.0.0',
    packages = find_packages(exclude=excludes),
    include_package_data = True,
    author = 'Intel(R) Corporation',
    author_email = 'tom.nabarro@intel.com',
    url = 'https://github.com/intel-hpdd/iml-common',
    description = 'Common library used by both agent and manager',
)
