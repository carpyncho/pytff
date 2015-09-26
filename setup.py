#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


#==============================================================================
# DOCS
#==============================================================================

"""This file is for distribute carpyncho pytff

"""


# =============================================================================
# IMPORTS
# =============================================================================

import sys

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages


#==============================================================================
# CONSTANTS
#==============================================================================

VERSION = ('0', '6', '15')

STR_VERSION = ".".join(VERSION)

REQUIREMENTS = ["numpy>=1.9", "sh>=1.11", "six==1.9"]

DESCRIPTION = "Wrapper arround G. Kovacs & G. Kupi Template Fourier Fitting"


#==============================================================================
# FUNCTIONS
#==============================================================================

def do_publish():
    import sh
    import six

    msg = "version {}".format(STR_VERSION)

    six.print_(sh.git.commit(a=True, m=msg))
    six.print_(sh.git.tag(a=STR_VERSION, m=msg))

    six.print_(sh.git.push("origin", "master"))
    six.print_(sh.git.push("origin", "master", tags=True))

    six.print_(sh.python("setup.py", "sdist", "upload"))

    msg = "Published version {}".format(STR_VERSION)
    six.print_(msg)


def do_setup():
    setup(
        name="pytff",
        version=STR_VERSION,
        description=DESCRIPTION,
        author="Juan BC",
        author_email="jbc.develop@gmail.com",
        url="https://github.com/carpyncho/pytff",
        license="3 Clause BSD",
        keywords="tff fourier template match",
        package_data={"pytff.datasets": ['dataset/*/*.*']},
        include_package_data=True,
        classifiers=(
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Physics",
            "Topic :: Scientific/Engineering :: Astronomy",
        ),
        packages=[pkg for pkg in find_packages() if pkg.startswith("pytff")],
        py_modules=["ez_setup"],
        install_requires=REQUIREMENTS,
    )


if __name__ == "__main__":
    if sys.argv[-1] == 'publish':
        do_publish()
    else:
        do_setup()
