#!/usr/bin/env python

"""The setup script."""


import pathlib
from setuptools import setup, Extension

readme = pathlib.Path("README.rst").read_text()
history = pathlib.Path("HISTORY.rst").read_text()
requirements = []
test_requirements = ["pytest>=3", ]

setup(
    author="Tri Songz, Sebastian Ziemann",
    author_email="ts@growthengineai.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Kubernetes Port-Forward Go-Edition For Python ",
    install_requires = requirements,
    license = "MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data = True,
    keywords = "portforward",
    name = "aioportforward",
    py_modules = [
        "aioportforward"
    ],
    test_suite="tests",
    tests_require=test_requirements,
    url = "https://github.com/trisongz/aioportforward",
    version = "0.0.1",
    zip_safe = False,
    # Go part
    setup_requires = ['setuptools-golang'],
    build_golang = {'root': 'github.com/trisongz/aioportforward'},
    ext_modules = [
        Extension(
            "_portforward", ["main.go"],
            py_limited_api = True, 
            define_macros = [('Py_LIMITED_API', None)],
        )
    ]
)
