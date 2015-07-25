#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: 3 Clause BSD
# Part of Carpyncho - http://carpyncho.jbcabral.org


# =============================================================================
# IMPORTS
# =============================================================================

import os
import tempfile
import hashlib
import uuid
from contextlib import contextmanager
from collections import namedtuple

import numpy as np

import sh

from . import constants


# =============================================================================
# COMMAND CLASS
# =============================================================================

class TFFCommand(object):

    def __init__(self, tff_path=constants.TFF_CMD, wrk_path=None, fmt="%.5f"):
        self._cmd = sh.Command(tff_path)
        self._fmt = fmt

        self._wrk_path = wrk_path or tempfile.mkdtemp(suffix="_tff")
        self._targets_path = os.path.join(self._wrk_path, "targets")

        self._lis_path = os.path.join(self._wrk_path, constants.LIS_FNAME)

        self._par_hash = None
        self._par_path = os.path.join(self._wrk_path, constants.PAR_FNAME)

        self._template_hash = None
        self._template_path = os.path.join(
            self._wrk_path, constants.TEMPLATE_FNAME)

        self._targets_cache = {}

        self._tff_dat_path = os.path.join(
            self._wrk_path, constants.TFF_DAT_FNAME)
        self._dff_dat_path = os.path.join(
            self._wrk_path, constants.DFF_DAT_FNAME)
        self._match_dat_path = os.path.join(
            self._wrk_path, constants.MATCH_DAT_FNAME)

    # =========================================================================
    # WRAPS
    # =========================================================================

    def __repr__(self):
        return "{} -> {}".format(repr(self._cmd), self._wrk_path)

    # =========================================================================
    # GETTERS
    # =========================================================================

    @property
    def wrk_path(self):
        return self._wrk_path

    @property
    def fmt(self):
        return self._fmt

    @property
    def cmd(self):
        return self._cmd

    @property
    def targets_cache(self):
        return self._targets_cache

    # =========================================================================
    # HELPERS
    # =========================================================================

    def hash(self, data):
        return hashlib.sha1(data).hexdigest()

    def clean(self, periods, times, values):
        periods = np.asarray(periods)
        times = np.asarray(times)
        values = np.asarray(values)

        pshape = periods.shape
        tshape = times.shape
        vshape = values.shape

        if len(pshape) != 1:
            raise ValueError("'periods' must be 1d array")
        elif tshape != vshape:
            raise ValueError("'times' and 'values' don have the same shape")

        msg = ("'times' and 'values' and times must "
               "be 2d array with same number rows as elements in 'periods'")
        if not (len(tshape) == len(vshape) == 2):
            raise ValueError(msg)
        elif not (periods.shape[0] == times.shape[0] == values.shape[0]):
            raise ValueError(msg)

        targets = np.dstack((times, values))

        return periods, targets

    # =========================================================================
    # IN PARSERS
    # =========================================================================

    def _render_par_file(self, **kwargs):

        def apply_format(**kwargs):
            formated = {}
            for k, v in kwargs.items():
                if isinstance(v, float):
                    fvalue = self._fmt % v
                else:
                    fvalue = str(v)
                while "." in fvalue and fvalue.endswith("0"):
                    fvalue = fvalue[:-1]
                formated[k] = fvalue
            return formated

        params = apply_format(**kwargs)
        src = constants.TFF_PAR_TEMPLATE.format(**params).strip()

        src_hash = self.hash(src)
        if self._par_hash is None or self._par_hash != src_hash:
            with open(self._par_path, "w") as fp:
                fp.write(src)
            self._par_hash = src_hash

    def _render_template_file(self):
        src = constants.TEMPLATE_DAT_SRC
        src_hash = self.hash(src)
        if self._template_hash is None or self._template_hash != src_hash:
            with open(self._template_path, "w") as fp:
                fp.write(src)
            self._template_hash = src_hash

    def _render_target_file(self, target):
        target_hash = self.hash(target)
        if target_hash not in self._targets_cache:
            uid = unicode(uuid.uuid1())
            fname = "{}.dat".format(uid)
            target_path = os.path.join(self._targets_path, fname)
            np.savetxt(target_path, target, fmt=self._fmt)
            self._targets_cache[target_hash] = target_path
        return self.targets_cache[target_hash]

    def _render_lis_file(self, periods, targets):
        with open(self._lis_path, "w") as fp:
            for idx, period in enumerate(periods):
                period = self._fmt % period
                target_path = self._render_target_file(targets[idx])
                line = constants.TARGET_LIS_LINE_TEMPLATE.format(
                    src_id=idx, period=period, target_path=target_path)
                fp.write(line)
                fp.write("\n")

    # =========================================================================
    # OUT PARSERS
    # =========================================================================

    def _read_fourier_dat(self, fp):

        def gen():
            buff = []
            for line in fp:
                # new source?
                if buff and not line.startswith(" "):
                    yield tuple(buff)
                    buff = []
                else:
                    buff.extend(line.strip().split())
            if buff:
                yield tuple(buff)

        fourier_dtypes = [
            ("src_idx", np.intp), ("period", np.float_),
            ("epoch", np.float_), ("average_magnitude", np.float_),
            ("number_of_data_points", np.float_), ("sigma_obs_fit", np.float_)]
        for idx in range(1,16):
            fourier_dtypes.append(("A_{}".format(idx), np.float_))
            fourier_dtypes.append(("phi_{}".format(idx), np.float_))

        fourier = np.fromiter(gen(), dtype=fourier_dtypes)
        return fourier

    def _load_tff_dat(self):
        with open(self._tff_dat_path) as fp:
            return self._read_fourier_dat(fp)

    def _load_dff_dat(self):
        with open(self._dff_dat_path) as fp:
            return self._read_fourier_dat(fp)

    def _load_match_dat(self, nmatch):

        def proc_buff(buff):
            src_idx, period, sigma, order, snr = (
                [(e,) * nmatch] for e in buff[:5])
            match_rank = [tuple(range(1, nmatch+1))]
            array = np.array(buff[5:])
            array.shape = (nmatch, 5)
            matchs = np.concatenate(
                (src_idx, match_rank, period, sigma, order, snr, array.T))
            return matchs.T

        def gen():
            buff, lineno = [], 0
            with open(self._match_dat_path) as fp:
                for line in fp:
                    buff.extend(line.strip().rsplit(None, 4))
                    lineno += 1
                    if lineno >= nmatch + 1:
                        for row in proc_buff(buff):
                            yield tuple(row)
                        buff = []
                        lineno = 0
            if buff:
                for row in proc_buff(buff):
                    yield tuple(row)

        match_dtypes = [
            ("src_idx", np.intp), ("match_rank", np.intp),
            ("src_period", np.float_), ("src_sigma_obs_fit", np.float_),
            ("order_of_the_template", np.intp),
            ("snr", np.float_), ("template_id", "S255"),
            ("template_period", np.float_),
            ("template_sigma_obs_fit", np.float_),
            ("src_N_data_point", np.int_), ("template_phi_31", np.float_)]
        matchs = np.fromiter(gen(), dtype=match_dtypes)

        return matchs


    # =========================================================================
    # CALL
    # =========================================================================

    def analize(self, periods, times, values,
                ntbin=300, nmin=10, mindp=10, snr1min=10.0,
                nmatch=10, dph=0.00001, asig=555.0, jfit=-1):

        periods, targets = self.clean(periods, times, values)

        # create the temp directories if its necesary
        if not os.path.isdir(self._targets_path):
            os.makedirs(self._targets_path)

        # create the parameters files
        self._render_lis_file(periods, targets)
        self._render_template_file()
        self._render_par_file(
            ntbin=ntbin, nmin=nmin, mindp=mindp, snr1min=snr1min,
            nmatch=nmatch, dph=dph, asig=asig, jfit=jfit)

        with cd(self._wrk_path):
            proc = self._cmd(
                constants.TEMPLATE_FNAME, constants.LIS_FNAME,
                constants.PAR_FNAME)
            proc.wait()

        tff_data = self._load_tff_dat()
        dff_data = self._load_dff_dat()
        match_data = self._load_match_dat(nmatch)

        return tff_data, dff_data, match_data

    def __call__(self, *args, **kwargs):
        return self.analize(*args, **kwargs)


# =============================================================================
# FUNCTIONS
# =============================================================================

@contextmanager
def cd(path):
    original = os.getcwdu()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original)
