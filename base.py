# Copyright (C) 2025 Mike Kuyper <mike@kuyper.us>. All rights reserved.
#
# This file is subject to the terms and conditions defined in file 'LICENSE',
# which is part of this source code package.

from typing import Any

import datetime as dt

from dataclasses import dataclass, KW_ONLY


def to_int(v:float, scale:float=1.0) -> int:
    return int(round(v / scale))


@dataclass
class GpsTime:
    week: int
    tow: int

    EPOCH = dt.datetime(1980, 1, 6, tzinfo=dt.UTC)
    SEC_PER_WEEK = (3600 * 24 * 7)

    def seconds(self) -> int:
        return (self.week * GpsTime.SEC_PER_WEEK) + self.tow

    def to_datetime(self, *, leaps:int=0) -> dt.datetime:
        return GpsTime.EPOCH + dt.timedelta(seconds=(self.seconds() - leaps))

    def rebase(self, base:'GpsTime|None'=None) -> 'GpsTime':
        if base is None:
            base = GpsTime.from_datetime(dt.datetime.now(tz=dt.UTC))
        base_s = base.seconds()
        return GpsTime.from_seconds(base_s + (self.tow - (base_s % self.SEC_PER_WEEK)))

    @staticmethod
    def from_seconds(seconds:int) -> 'GpsTime':
        week, tow = divmod(seconds, GpsTime.SEC_PER_WEEK)
        return GpsTime(week, tow)

    @staticmethod
    def from_datetime(t:dt.datetime, *, leaps:int=0) -> 'GpsTime':
        delta_s = int((t - GpsTime.EPOCH).total_seconds()) + leaps

        return GpsTime.from_seconds(delta_s)


@dataclass
class Ephemeris:
    svid: int

    fit_interval: bool
    ura_index: int
    sv_health: int
    tgd: float          # s
    iodc: int
    toc: int            # s (time-of-week)
    af2: float          # s/s²
    af1: float          # s/s
    af0: float          # s
    crs: float          # m
    delta_n: float      # semicircles/s
    m0: float           # semicircles
    cuc: float          # radians
    cus: float          # radians
    e: float            # n/a
    sqrt_a: float       # √m
    toe: int            # s (time-of-week)
    cic: float          # radians
    omega0: float       # semicircles
    cis: float          # radians
    crc: float          # m
    i0: float           # semicircles
    omega: float        # semicircles
    omega_dot: float    # semicircles/s
    idot: float         # semicircles/s

    _: KW_ONLY

    _reftime: GpsTime|None = None   # Reference time (to help resolve TOW values)
