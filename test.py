#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


#==============================================================================
# DOCS
#==============================================================================

"""This file is for test carpyncho pytff

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import unittest
import csv

import six

import numpy as np

import pytff


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))


# =============================================================================
# TEST CASES
# =============================================================================

class PyTFFFunctionTest(unittest.TestCase):

    def test_loadtarget(self):
        data = "1 2\n3 4\n5 6"
        fp = six.StringIO(data)
        times_values = pytff.loadtarget(fp)
        for lidx, line in enumerate(data.splitlines()):
            for cidx, value in enumerate(line.split()):
                fvalue = float(value)
                pytff_value = times_values[cidx][0][lidx]
                np.testing.assert_allclose(fvalue, pytff_value)


class PyTFFCommandTest(unittest.TestCase):

    def setUp(self):
        self.tff = pytff.TFFCommand()

    def assertFourierEquals(self, pytff_data, fpath, **kwargs):
        original = ["0"]
        with open(fpath) as fp:
            reader = csv.reader(fp, delimiter=" ")
            for lidx, line in enumerate(reader):
                if lidx == 0:
                    continue
                original += [e for e in line if e.strip()]
        for pytff_value, orig_value in six.moves.zip(pytff_data[0], original):
            orig_value = pytff_value.dtype.type(orig_value)
            np.testing.assert_allclose(orig_value, pytff_value, **kwargs)

    def assertMatchEquals(self, match_data, fpath, **kwargs):
        original = []
        with open(fpath) as fp:
            reader = csv.reader(fp, delimiter=" ")
            header = None
            for lidx, line in enumerate(reader):
                line = " ".join(line).strip().rsplit(None, 4)
                if lidx == 0:
                    header = line[1:]
                else:
                    original.append(["0", lidx] + header + line)

        for mline, oline in six.moves.zip(match_data, original):
            for mvalue, ovalue in six.moves.zip(mline, oline):
                dtype = mvalue.dtype.type
                ovalue = dtype(ovalue)
                if dtype == np.string_:
                    self.assertEquals(
                        mvalue, ovalue, msg=kwargs.get("err_msg"))
                else:
                    np.testing.assert_allclose(ovalue, mvalue, **kwargs)

    def test_ogle_data(self):
        ogle_path = os.path.join(PATH, "data", "ogle.dat")
        ogle_tff_path = os.path.join(PATH, "data", "ogle_tff.dat")
        ogle_dff_path = os.path.join(PATH, "data", "ogle_dff.dat")
        ogle_match_path = os.path.join(PATH, "data", "ogle_match.dat")

        times, values = pytff.loadtarget(ogle_path)
        periods = np.array([0.6347522])

        tff_data, dff_data, match_data = self.tff.analyze(
            periods, times, values)

        self.assertFourierEquals(
            tff_data, ogle_tff_path, err_msg="tff is diferent")
        self.assertFourierEquals(
            dff_data, ogle_dff_path, err_msg="dff is diferent")
        self.assertMatchEquals(
            match_data, ogle_match_path, err_msg="match is diferent")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
