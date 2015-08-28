#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# FUTURES
# =============================================================================

from __future__ import unicode_literals


# =============================================================================
# DOC
# =============================================================================

__doc__ = """PyTFF datasets"""


# =============================================================================
# IMPORTS
# =============================================================================

import os


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))


# =============================================================================
# FUNCTIONS
# =============================================================================

def get(datasetname, filename):
    """Retrieve a full path to datasetfile or raises an IOError"""
    path = os.path.join(PATH, datasetname, filename)
    if os.path.exists(path):
        return path
    raise IOError("Resource '{}' not exists".format(path))


def ls():
    """List all existing datasests in dictiornay where every key is a dataset
    name and a value is file of this dataset

    """
    files = {}
    for dirpath, dirnames, filenames in os.walk(PATH):
        if dirpath != PATH and not os.path.basename(dirpath).startswith("_"):
            container = files.setdefault(dirpath, [])
            container.extend(filenames)
    return files


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
