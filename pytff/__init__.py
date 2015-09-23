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

from .core import (  # noqa
    TFFCommand, loadtarget, stack_targets,
    load_tff_dat, load_match_dat, cache_hash, fspace)
