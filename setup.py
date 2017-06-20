#!/usr/bin/env python
# Copyright (c) 2017 Intel Corporation. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.


from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

excludes = ["*tests*"]

setup(
    name='iml-common',
    use_scm_version=True,
    skip_upload_docs=True,
    setup_requires=['setuptools_scm'],
    license='MIT',
    packages=find_packages(exclude=excludes),
    include_package_data=True,
    author='Intel(R) Corporation',
    author_email='tom.nabarro@intel.com',
    url='https://github.com/intel-hpdd/iml-common',
    description='Common library used by multiple IML component',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Lustre administrators',
        'Topic :: Software Development :: Integrated Management Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='IML lustre high-availability',
)
