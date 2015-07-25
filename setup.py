#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


#==============================================================================
# DOCS
#==============================================================================

"""This file is for distribute carpyncho pytff

"""

#==============================================================================
# CONSTANTS
#==============================================================================

REQUIREMENTS = ["numpy>=1.9", "sh>=1.11"]


#==============================================================================
# FUNCTIONS
#==============================================================================

if __name__ == "__main__":
    import os
    import sys

    from ez_setup import use_setuptools
    use_setuptools()

    from setuptools import setup, find_packages

    import pytff

    setup(
        name="pytff",
        version=pytff.get_version(),
        description=pytff.__doc__.splitlines()[0],
        author="Juan BC",
        author_email="jbc.develop@gmail.com",
        url="https://github.com/carpyncho/pytff",
        license="3 Clause BSD",
        keywords="tff fourier template match",
        classifiers=(
            "Topic :: Utilities",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 2",
        ),
        packages=[pkg for pkg in find_packages() if pkg.startswith("pytff")],
        py_modules=["ez_setup"],
        install_requires=REQUIREMENTS,
    )
