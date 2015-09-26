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
import tempfile
import shutil
import random
import uuid

import six

import numpy as np

import sh

import pytff
from . import datasets, constants


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))


# =============================================================================
# TEST CASES
# =============================================================================

class DatasetTest(unittest.TestCase):

    def setUp(self):
        self.datasets_path = os.path.join(PATH, "datasets")
        self.files = {}
        for dirpath, dirnames, filenames in os.walk(self.datasets_path):
            basename = os.path.basename(dirpath)
            if dirpath != self.datasets_path and not basename.startswith("_"):
                    container = self.files.setdefault(basename, [])
                    container.extend(
                        fn for fn in filenames if not fn.startswith("_"))

    def test_ls(self):
        self.assertEqual(self.files, datasets.ls())

    def test_info(self):
        for dataset in six.iterkeys(self.files):
            info = datasets.info(dataset)
            path = os.path.join(datasets.PATH, dataset, "_info.txt")
            if info and os.path.isfile(path):
                with open(path) as fp:
                    self.assertEqual(info, fp.read())
            elif not info:
                self.fail("info of '{}' don't match".format(dataset))

    def test_get(self):
        for dirpath, filenames in self.files.items():
            for fname in filenames:
                datasets.get(dirpath, fname)
        dirpath = random.choice(list(self.files.keys()))
        fname = random.choice(self.files[dirpath])
        datasets.get(dirpath, fname)
        with self.assertRaises(IOError):
            datasets.get(dirpath, fname + "_")
        with self.assertRaises(IOError):
            datasets.get(dirpath + "_", fname)
        with self.assertRaises(IOError):
            datasets.get(dirpath + "_", fname + "_")


class FunctionTest(unittest.TestCase):

    def test_fspace(self):
        start, stop, num = 0, 2 * np.pi, 1000

        ffs = [
            {"period": 2. * np.pi,
             "A_1": 1, "A_2": 0, "A_3": 0, "A_4": 0, "A_5": 0, "A_6": 0,
             "A_7": 0, "A_8": 0, "A_9": 0, "A_10": 0, "A_11": 0, "A_12": 0,
             "A_13": 0, "A_14": 0, "A_15": 0,
             "phi_1": 0, "phi_2": 0, "phi_3": 0, "phi_4": 0, "phi_5": 0,
             "phi_6": 0, "phi_7": 0, "phi_8": 0, "phi_9": 0, "phi_10": 0,
             "phi_11": 0, "phi_12": 0, "phi_13": 0, "phi_14": 0, "phi_15": 0},

            {"period": 4. * np.pi,
             "A_1": 1, "A_2": 0, "A_3": 0, "A_4": 0, "A_5": 0, "A_6": 0,
             "A_7": 0, "A_8": 0, "A_9": 0, "A_10": 0, "A_11": 0, "A_12": 0,
             "A_13": 0, "A_14": 0, "A_15": 0,
             "phi_1": 0, "phi_2": 0, "phi_3": 0, "phi_4": 0, "phi_5": 0,
             "phi_6": 0, "phi_7": 0, "phi_8": 0, "phi_9": 0, "phi_10": 0,
             "phi_11": 0, "phi_12": 0, "phi_13": 0, "phi_14": 0, "phi_15": 0},

            {"period": 2. * np.pi,
             "A_1": 1, "A_2": 0, "A_3": 0, "A_4": 0, "A_5": 0, "A_6": 0,
             "A_7": 0, "A_8": 0, "A_9": 0, "A_10": 0, "A_11": 0, "A_12": 0,
             "A_13": 0, "A_14": 0, "A_15": 0,
             "phi_1": 2, "phi_2": 0, "phi_3": 0, "phi_4": 0, "phi_5": 0,
             "phi_6": 0, "phi_7": 0, "phi_8": 0, "phi_9": 0, "phi_10": 0,
             "phi_11": 0, "phi_12": 0, "phi_13": 0, "phi_14": 0, "phi_15": 0}
        ]

        sinx_fs = [1, 0.5, 1]
        sinx_ps = [0, 0, 2]

        for ff, sinx_f, sinx_p in zip(ffs, sinx_fs, sinx_ps):
            x, y = pytff.fspace(ff, start, stop, num)
            sinx = np.linspace(start, stop, num)
            siny = np.sin(sinx * sinx_f + sinx_p)

            self.assertEquals(len(x), num)
            self.assertEquals(len(x), len(sinx))
            np.testing.assert_allclose(x, sinx)
            self.assertEquals(len(y), num)
            self.assertEquals(len(y), len(siny))
            np.testing.assert_allclose(y, siny)

            # with retstep
            x, y, retstep = pytff.fspace(ff, start, stop, num, retstep=True)
            sinx, sinrstep = np.linspace(start, stop, num, retstep=True)
            siny = np.sin(sinx * sinx_f + sinx_p)

            self.assertEquals(len(x), num)
            self.assertEquals(len(x), len(sinx))
            np.testing.assert_allclose(x, sinx)
            self.assertEquals(len(y), num)
            self.assertEquals(len(y), len(siny))
            np.testing.assert_allclose(y, siny)
            self.assertEqual(retstep, sinrstep)

    def test_cache_hash(self):
        data = [
            six.text_type(random.random()),
            np.random.randn(10), six.b("hhh"), "hhh"]
        for elem in data:
            pytff.cache_hash(elem)

    def test_loadtarget(self):
        data = "1 2\n3 4\n5 6"
        fp = six.StringIO(data)
        times_values = pytff.loadtarget(fp)
        for lidx, line in enumerate(data.splitlines()):
            for cidx, value in enumerate(line.split()):
                fvalue = float(value)
                pytff_value = times_values[cidx][0][lidx]
                np.testing.assert_allclose(fvalue, pytff_value)

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

    def test_stack_targets_empty(self):
        expected_times = np.array([[], []])
        expected_values = np.array([[], []])

        times = [[], []]
        values = [[], []]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        times = [np.array([]), []]
        values = [[], np.array([])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        times = [np.array([]), np.array([])]
        values = [np.array([]), np.array([])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        expected_times = np.array([[np.nan], [1]])
        expected_values = np.array([[np.nan], [1]])
        times = [np.array([]), np.array([1])]
        values = [np.array([]), np.array([1])]
        stk_times, stk_values = pytff.stack_targets(times, values)
        np.testing.assert_array_equal(stk_times, expected_times)
        np.testing.assert_array_equal(stk_values, expected_values)

        times = np.array([[], [1]])
        values = np.array([[], [1]])
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

    def test_load_tff_dat(self):
        ogle_tff_path = datasets.get("single_dat", "tff.dat")

        asstring = pytff.load_tff_dat(ogle_tff_path)
        with open(ogle_tff_path) as fp:
            asfp = pytff.load_tff_dat(fp)
        self.assertEqual(asstring, asfp)
        self.assertIsInstance(asstring, tuple)
        self.assertIsInstance(asfp, tuple)
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asstring)))
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asfp)))

        rnd = random.random()
        asstring = pytff.load_tff_dat(ogle_tff_path, lambda gen: rnd)
        with open(ogle_tff_path) as fp:
            asfp = pytff.load_tff_dat(fp, lambda gen: rnd)
        self.assertEqual(asstring, asfp)
        self.assertEqual(asfp, rnd)
        self.assertEqual(asstring, rnd)

    def test_load_match_dat(self):
        ogle_mch_path = datasets.get("single_dat", "match.dat")

        asstring = pytff.load_match_dat(ogle_mch_path)
        with open(ogle_mch_path) as fp:
            asfp = pytff.load_match_dat(fp)
        self.assertEqual(asstring, asfp)
        self.assertIsInstance(asstring, tuple)
        self.assertIsInstance(asfp, tuple)
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asstring)))
        self.assertTrue(all(map(lambda e: isinstance(e, tuple), asfp)))

        rnd = random.random()
        asstring = pytff.load_match_dat(ogle_mch_path, lambda gen: rnd)
        with open(ogle_mch_path) as fp:
            asfp = pytff.load_match_dat(fp, lambda gen: rnd)
        self.assertEqual(asstring, asfp)
        self.assertEqual(asfp, rnd)
        self.assertEqual(asstring, rnd)


class TFFCommandTest(unittest.TestCase):

    def setUp(self):
        self.tff = pytff.TFFCommand()

    def test_repr(self):
        repr(self.tff)

    def test_invalid_input_data(self):
        msg = "'periods' must be 1d array"
        with six.assertRaisesRegex(self, ValueError, msg):
            self.tff.analyze([[]], [], [])

        msg = "'times' and 'values' don have the same shape"
        with six.assertRaisesRegex(self, ValueError, msg):
                self.tff.analyze([1], [[1]], [[2], [3]])

        msg = (
            "'times' and 'values' must "
            "be 2d array with same number rows as elements in 'periods'")
        with six.assertRaisesRegex(self, ValueError, msg):
                self.tff.analyze([1], [1], [2])
        with six.assertRaisesRegex(self, ValueError, msg):
                self.tff.analyze([1, 2], [[1]], [[2]])

    def test_wrk_path(self):
        wrk_path = six.text_type(uuid.uuid1()) + six.text_type(random.random())
        self.tff = pytff.TFFCommand(wrk_path=wrk_path)
        self.assertEqual(self.tff.wrk_path, wrk_path)

        coriginal = constants.WRK_PATH
        wrk_path = six.text_type(uuid.uuid1()) + six.text_type(random.random())
        try:
            constants.WRK_PATH = wrk_path
            self.tff = pytff.TFFCommand()
            self.assertEqual(self.tff.wrk_path, wrk_path)
        finally:
            constants.WRK_PATH = coriginal

    def test_tff_path(self):
        self.assertEqual(self.tff.cmd, sh.Command(constants.TFF_CMD))

        tff_path = 'ls'
        self.tff = pytff.TFFCommand(tff_path=tff_path)
        self.assertEqual(self.tff.cmd, sh.Command(tff_path))

    def test_fmt(self):
        self.assertEqual(self.tff.fmt, "%.5f")

        fmt = six.text_type(uuid.uuid1()) + six.text_type(random.random())
        self.tff = pytff.TFFCommand(fmt=fmt)
        self.assertEqual(self.tff.fmt, fmt)

    def test_single_data(self):
        ogle_path = datasets.get("single_dat", "ogle.dat")
        ogle_tff_path = datasets.get("single_dat", "tff.dat")
        ogle_dff_path = datasets.get("single_dat", "dff.dat")
        ogle_mch_path = datasets.get("single_dat", "match.dat")

        ogle_tff = pytff.load_tff_dat(ogle_tff_path, self.tff.process_tff)
        ogle_dff = pytff.load_tff_dat(ogle_dff_path, self.tff.process_dff)
        ogle_mch = pytff.load_match_dat(ogle_mch_path, self.tff.process_matchs)

        times, values = pytff.loadtarget(ogle_path)
        periods = np.array([0.6347522])

        tff_data, dff_data, mch_data = self.tff.analyze(periods, times, values)

        np.testing.assert_array_equal(tff_data, ogle_tff)
        np.testing.assert_array_equal(dff_data, ogle_dff)
        np.testing.assert_array_equal(mch_data, ogle_mch)

    def test_split_data(self):
        ogle_0_path = datasets.get("split_dat", "ogle_0.dat")
        ogle_1_path = datasets.get("split_dat", "ogle_1.dat")
        ogle_tff_path = datasets.get("split_dat", "tff.dat")
        ogle_dff_path = datasets.get("split_dat", "dff.dat")
        ogle_mch_path = datasets.get("split_dat", "match.dat")

        ogle_tff = pytff.load_tff_dat(ogle_tff_path, self.tff.process_tff)
        ogle_dff = pytff.load_tff_dat(ogle_dff_path, self.tff.process_dff)
        ogle_mch = pytff.load_match_dat(ogle_mch_path, self.tff.process_matchs)

        times_0, values_0 = pytff.loadtarget(ogle_0_path)
        times_1, values_1 = pytff.loadtarget(ogle_1_path)
        times, values = pytff.stack_targets(
            (times_0, times_1), (values_0, values_1))
        periods = np.array([0.6347522] * 2)

        tff_data, dff_data, mch_data = self.tff.analyze(periods, times, values)

        np.testing.assert_array_equal(tff_data, ogle_tff)
        np.testing.assert_array_equal(dff_data, ogle_dff)
        np.testing.assert_array_equal(mch_data, ogle_mch)

    def test_diferent_shape_data(self):
        # this test only verify nothing blows up
        periods = [1, 2]
        times = [[0, 1, 2], [3, 4, 5, 6]]
        values = [[0, 1, 2], [3, 4, 5, 7]]
        self.tff.analyze(periods, times, values)

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

    def test_write_stk_targets(self):
        periods = [1, 2]
        times = [[0, 1, 2], [3, 4, 5, 6]]
        values = [[0, 1, 2], [3, 4, 5, 7]]
        self.tff.debug = True
        self.tff.analyze(periods, times, values)

        targets = np.dstack(pytff.stack_targets(times, values))
        for idx, t in enumerate(targets):
            ch = pytff.cache_hash(t)
            self.assertIn(ch, self.tff.targets_cache)
            with open(self.tff.targets_cache[ch]) as fp:
                linenos = len(fp.readlines())
            self.assertTrue(len(times[idx]) == len(values[idx]) == linenos)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    unittest.main()
