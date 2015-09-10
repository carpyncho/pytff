#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


# =============================================================================
# IMPORTS
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
import codecs


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))


# =============================================================================
# FUNCTIONS
# =============================================================================

def get(datasetname, filename):
    """Retrieve a full path to datasetfile or raises an IOError

    """
    path = os.path.join(PATH, datasetname, filename)
    if (datasetname and filename and not
       datasetname.startswith("_") and not filename.startswith("_") and
       os.path.isfile(path)):
            return path
    raise IOError("Dataset file '{}' not exists".format(path))


def info(datasetname):
    """Return information about a given dataset as plain text

    """
    dspath = os.path.join(PATH, datasetname)
    path = os.path.join(dspath, "_info.txt")
    if os.path.isdir(dspath):
        infotext = u""
        if os.path.isfile(path):
            with codecs.open(path, encoding="utf8") as fp:
                infotext = fp.read()
        return infotext
    raise IOError("Dataset do not exists")


def ls():
    """List all existing datasests in dictiornay where every key is a dataset
    name and a value is file of this dataset

    """
    files = {}
    for dirpath, dirnames, filenames in os.walk(PATH):
        basename = os.path.basename(dirpath)
        if dirpath != PATH and not basename.startswith("_"):
            container = files.setdefault(basename, [])
            container.extend(
                fn for fn in filenames if not fn.startswith("_"))
    return files
