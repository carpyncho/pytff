#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


# =============================================================================
# DOCS
# =============================================================================

"""This file is for test carpyncho pytff

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import unittest
import csv
import tempfile
import shutil

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

    def assertFourierEquals(self, pytff_data, fpath, original, **kwargs):
        original = [six.text_type(original)]
        with open(fpath) as fp:
            reader = csv.reader(fp, delimiter=" ")
            for lidx, line in enumerate(reader):
                if lidx == 0:
                    continue
                original += [e for e in line if e.strip()]
        for pytff_value, orig_value in six.moves.zip(pytff_data[0], original):
            orig_value = pytff_value.dtype.type(orig_value)
            np.testing.assert_allclose(orig_value, pytff_value, **kwargs)

    def assertMatchEquals(self, match_data, fpath, original, **kwargs):
        org_first = original
        original = []
        with open(fpath) as fp:
            reader = csv.reader(fp, delimiter=" ")
            header = None
            for lidx, line in enumerate(reader):
                line = " ".join(line).strip().rsplit(None, 4)
                if lidx == 0:
                    header = line[1:]
                else:
                    original.append([org_first, lidx] + header + line)

        for mline, oline in six.moves.zip(match_data, original):
            for mvalue, ovalue in six.moves.zip(mline, oline):
                dtype = mvalue.dtype.type
                ovalue = dtype(ovalue)
                if dtype == np.string_:
                    self.assertEqual(
                        mvalue, ovalue, msg=kwargs.get("err_msg"))
                else:
                    np.testing.assert_allclose(ovalue, mvalue, **kwargs)

    def _test_single_data(self):
        data_path = os.path.join(PATH, "data", "single_dat")
        ogle_path = os.path.join(data_path, "ogle.dat")
        ogle_tff_path = os.path.join(data_path, "tff.dat")
        ogle_dff_path = os.path.join(data_path, "dff.dat")
        ogle_match_path = os.path.join(data_path, "match.dat")

        times, values = pytff.loadtarget(ogle_path)
        periods = np.array([0.6347522])

        tff_data, dff_data, match_data = self.tff.analyze(
            periods, times, values)

        self.assertFourierEquals(
            tff_data, ogle_tff_path, 0, err_msg="tff is diferent")
        self.assertFourierEquals(
            dff_data, ogle_dff_path, 0, err_msg="dff is diferent")
        self.assertMatchEquals(
            match_data, ogle_match_path, 0, err_msg="match is diferent")

    def test_split_data(self):
        data_path = os.path.join(PATH, "data", "split_dat")
        ogle_0_path = os.path.join(data_path, "ogle_0.dat")
        ogle_1_path = os.path.join(data_path, "ogle_1.dat")
        ogle_tff_path = os.path.join(data_path, "tff.dat")
        ogle_dff_path = os.path.join(data_path, "dff.dat")
        ogle_match_path = os.path.join(data_path, "match.dat")

        times_0, values_0 = pytff.loadtarget(ogle_0_path)
        times_1, values_1 = pytff.loadtarget(ogle_1_path)

        times, values = pytff.stack_targets(
            (times_0, times_1), (values_0[0], values_1))
        periods = np.array([0.6347522] * 2)

        tff_data, dff_data, match_data = self.tff.analyze(
            periods, times, values)

        import ipdb; ipdb.set_trace()


    def test_diferent_shape_data(self):
        # this test only verify nothing blows up
        periods = [1, 2]
        times = [[0, 1, 2], [3, 4, 5, 6]]
        values = [[0, 1, 2], [3, 4, 5, 7]]
        self.tff.analyze(periods, times, values)

    def test_stack_targets_diferent_sizes(self):
        # Diferent sizes
        times = [[0, 1, 2], [3, 4, 5, 6]]
        expected_times = np.array([[0., 1., 2., np.nan],
                                   [3., 4., 5., 6.]])

        values = [[0, 1, 2], [3, 4, 5, 7]]
        expected_values = np.array([[0., 1., 2., np.nan],
                                    [3., 4., 5., 7.]])

        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # diferent sizes array
        times = [np.array([0, 1, 2]), np.array([3, 4, 5, 6])]
        values = [np.array([0, 1, 2]), np.array([3, 4, 5, 7])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # more dimensions
        times = [np.array([[0, 1, 2]]), np.array([[3, 4, 5, 6]])]
        values = [np.array([[0, 1, 2]]), np.array([[3, 4, 5, 7]])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

    def test_stack_targets_same_sizes(self):
        times = [[0, 1, 2], [3, 4, 5]]
        expected_times = np.array([[0., 1., 2.],
                                   [3., 4., 5.]])

        values = [[0, 1, 2], [3, 4, 5]]
        expected_values = np.array([[0., 1., 2.],
                                    [3., 4., 5.]])

        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # same sizes array
        times = [np.array([0, 1, 2]), np.array([3, 4, 5])]
        values = [np.array([0, 1, 2]), np.array([3, 4, 5])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        # arrays more dimensions
        times = [np.array([[0, 1, 2]]), np.array([[3, 4, 5]])]
        values = [np.array([[0, 1, 2]]), np.array([[3, 4, 5]])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

    def test_wrkpath_is_removed_when_is_temp(self):
        # remove clasic temp
        path = self.tff.wrk_path
        self.assertTrue(os.path.exists(path) and os.path.isdir(path))
        del self.tff
        self.assertFalse(os.path.exists(path) and os.path.isdir(path))

    def test_wrkpath_is_not_removed_when_is_not_temp(self):
        path = tempfile.mkdtemp(suffix="_tff_test")

        self.tff = pytff.TFFCommand(wrk_path=path)
        self.assertTrue(os.path.exists(path) and os.path.isdir(path))
        del self.tff
        self.assertTrue(os.path.exists(path) and os.path.isdir(path))

        shutil.rmtree(path, True)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    unittest.main()
