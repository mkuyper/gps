# Copyright (C) 2025 Mike Kuyper <mike@kuyper.us>. All rights reserved.
#
# This file is subject to the terms and conditions defined in file 'LICENSE',
# which is part of this source code package.

import datetime as dt
import math
import re
import xarray as xr

from .base import Ephemeris, GpsTime

class RinexUtil:
    RE_SVID = re.compile(r'G\d\d')

    @staticmethod
    def svid(r:xr.Dataset) -> int:
        s = r.sv.item()
        if RinexUtil.RE_SVID.match(s) is None:
            raise ValueError(f'Invalid SV: {s}')
        return int(s[1:])

    @staticmethod
    def toc(r:xr.Dataset) -> GpsTime:
        t = dt.datetime.fromtimestamp(r.time.item() / 1e9, tz=dt.UTC)
        return GpsTime.from_datetime(t)

    @staticmethod
    def ura_index(r:xr.Dataset) -> int:
        acc = RinexUtil.value(r.SVacc)

        thresholds = { 2.4, 3.4, 4.85, 6.85, 9.65, 13.65, 24, 48,
                      96, 192, 384, 768, 1536, 3072, 6144 }

        for i, th in enumerate(thresholds):
            if acc <= th:
                return i
        return 15

    @staticmethod
    def value(r:xr.Dataset|xr.DataArray) -> float:
        v = float(r.item())
        if math.isnan(v):
            raise ValueError(f'Missing value {r}')
        return v


class Rinex:
    @staticmethod
    def ephemeris_from_rinex(r:xr.Dataset) -> Ephemeris:
        if r.rinextype != 'nav':
            raise ValueError(f'Unexpected RINEX type "{r.rinextype}"')
        toc = RinexUtil.toc(r)
        return Ephemeris(
                svid = RinexUtil.svid(r),
                fit_interval = False if int(RinexUtil.value(r.FitIntvl)) == 4 else True,
                ura_index = RinexUtil.ura_index(r),
                sv_health = int(RinexUtil.value(r.health)),
                tgd = RinexUtil.value(r.TGD),
                iodc = int(RinexUtil.value(r.IODC)),
                toc = toc.tow,
                af2 = RinexUtil.value(r.SVclockDriftRate),
                af1 = RinexUtil.value(r.SVclockDrift),
                af0 = RinexUtil.value(r.SVclockBias),
                crs = RinexUtil.value(r.Crs),
                delta_n = RinexUtil.value(r.DeltaN) / math.pi,
                m0 = RinexUtil.value(r.M0) / math.pi,
                cuc = RinexUtil.value(r.Cuc),
                cus = RinexUtil.value(r.Cus),
                e = RinexUtil.value(r.Eccentricity),
                sqrt_a = RinexUtil.value(r.sqrtA),
                toe = int(RinexUtil.value(r.Toe)),
                cic = RinexUtil.value(r.Cic),
                omega0 = RinexUtil.value(r.Omega0) / math.pi,
                cis = RinexUtil.value(r.Cis),
                crc = RinexUtil.value(r.Crc),
                i0 = RinexUtil.value(r.Io) / math.pi,
                omega = RinexUtil.value(r.omega) / math.pi,
                omega_dot = RinexUtil.value(r.OmegaDot) / math.pi,
                idot = RinexUtil.value(r.IDOT) / math.pi,

                _reftime=toc)
