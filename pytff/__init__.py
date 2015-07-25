#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


# =============================================================================
# DOC
# =============================================================================

"""Wrapper arround G. Kovacs & G. Kupi Template Fourier Fitting

For more info please check: http://www.konkoly.hu/staff/kovacs/tff.html

"""

# =============================================================================
# IMPORTS
# =============================================================================

import inspect

from .core import TFFCommand

# =============================================================================
# CONSTANTS and confs
# =============================================================================

VERSION = ('0', '1')

__version__ = ".".join(VERSION)


# =============================================================================
# FUNCTIONS
# =============================================================================

def get_version():
    return __version__

