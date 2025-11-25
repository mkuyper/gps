# Copyright (C) 2025 Mike Kuyper <mike@kuyper.us>. All rights reserved.
#
# This file is subject to the terms and conditions defined in file 'LICENSE',
# which is part of this source code package.

import cstruct

from .base import Ephemeris, to_int

NrfModemGnssAgpsDataEphemeris = cstruct.parse('''
    /** @brief A-GPS ephemeris data. */
    struct nrf_modem_gnss_agps_data_ephemeris {
        /** Satellite ID (dimensionless). Range 1...32. */
        uint8_t sv_id;
        /** Satellite health (dimensionless). */
        uint8_t health;
        /** Issue of data, clock parameters (dimensionless). Range 0...2047 (11 bits). */
        uint16_t iodc;
        /** Clock parameters reference GPS time-of-week (sec). Scale factor 2^4. Range 0...37799. */
        uint16_t toc;
        /** Clock drift rate (sec/sec2). Scale factor 2^-55. */
        int8_t af2;
        /** Clock drift (sec/sec). Scale factor 2^-43. */
        int16_t af1;
        /** Clock bias (sec). Scale factor 2^-31. Range -2097152...2097151 (22 bit) */
        int32_t af0;
        /** Group delay (sec). Scale factor 2^-31. */
        int8_t tgd;
        /** URA index (dimensionless). Range 0...15. */
        uint8_t ura;
        /** Curve fit interval indication. Range 0...1. */
        uint8_t fit_int;
        /** Ephemeris parameters reference GPS time-of-week (sec). Scale factor 2^4. Range 0...37799. */
        uint16_t toe;
        /** Argument of perigee (semi-circle). Scale factor 2^-31. */
        int32_t w;
        /** Mean motion difference (semi-circle/sec). Scale factor 2^-43. */
        int16_t delta_n;
        /** Mean anomaly at reference time (semi-circle). Scale factor 2^-31. */
        int32_t m0;
        /** Rate of right ascension (semi-circle/sec). Scale factor 2^-43. Range -8388608...8388607 (24 bits). */
        int32_t omega_dot;
        /** Eccentricity (dimensionless). Scale factor 2^-33. */
        uint32_t e;
        /** Rate of inclination angle (semi-circle/sec). Scale factor 2-43. Range -8192...8191 (14 bits). */
        int16_t idot;
        /** Square root of semi-major axis (m). Scale factor 2^-19. */
        uint32_t sqrt_a;
        /** Inclination angle at reference time (semi-circle). Scale factor 2^-31. */
        int32_t i0;
        /** Longitude of ascending node at weekly epoch (semi-circle). Scale factor 2^-31. */
        int32_t omega0;
        /** Orbit radius, sine harmonic amplitude (m). Scale factor 2^-5. */
        int16_t crs;
        /** Inclination angle, sine harmonic amplitude (rad). Scale factor 2^-29. */
        int16_t cis;
        /** Argument of latitude, sine harmonic amplitude (rad). Scale factor 2^-29. */
        int16_t cus;
        /** Orbit radius, cosine harmonic amplitude (m). Scale factor 2^-5. */
        int16_t crc;
        /** Inclination angle, cosine harmonic amplitude (rad). Scale factor 2^-29. */
        int16_t cic;
        /** Argument of latitude, cosine harmonic amplitude (rad). Scale factor 2^-29. */
        int16_t cuc;
    };
''')

class NrfModemGnssAgps:
    @staticmethod
    def load_ephemeris(data:bytes) -> cstruct.MemCStruct:
        ne = NrfModemGnssAgpsDataEphemeris()
        ne.unpack(data)
        return ne

    @staticmethod
    def create_ephemeris(e:Ephemeris) -> cstruct.MemCStruct:
        ne = NrfModemGnssAgpsDataEphemeris()

        # Satellite ID (dimensionless). Range 1...32.
        ne.sv_id = e.svid
        # Satellite health (dimensionless).
        ne.health = e.sv_health
        # Issue of data, clock parameters (dimensionless). Range 0...2047 (11 bits).
        ne.iodc = e.iodc
        # Clock parameters reference GPS time-of-week (sec). Scale factor 2^4. Range 0...37799.
        ne.toc = e.toc // 16
        # Clock drift rate (sec/sec2). Scale factor 2^-55.
        ne.af2 = to_int(e.af2, 2**-55)
        # Clock drift (sec/sec). Scale factor 2^-43.
        ne.af1 = to_int(e.af1, 2**-43)
        # Clock bias (sec). Scale factor 2^-31. Range -2097152...2097151 (22 bit)
        ne.af0 = to_int(e.af0, 2**-31)
        # Group delay (sec). Scale factor 2^-31.
        ne.tgd = to_int(e.tgd, 2**-31)
        # URA index (dimensionless). Range 0...15.
        ne.ura = e.ura_index
        # Curve fit interval indication. Range 0...1.
        ne.fit_int = 1 if e.fit_interval else 0
        # Ephemeris parameters reference GPS time-of-week (sec). Scale factor 2^4. Range 0...37799.
        ne.toe = e.toe // 16
        # Argument of perigee (semi-circle). Scale factor 2^-31.
        ne.w = to_int(e.omega, 2**-31)
        # Mean motion difference (semi-circle/sec). Scale factor 2^-43.
        ne.delta_n = to_int(e.delta_n, 2**-43)
        # Mean anomaly at reference time (semi-circle). Scale factor 2^-31.
        ne.m0 = to_int(e.m0, 2**-31)
        # Rate of right ascension (semi-circle/sec). Scale factor 2^-43. Range -8388608...8388607 (24 bits).
        ne.omega_dot = to_int(e.omega_dot, 2**-43)
        # Eccentricity (dimensionless). Scale factor 2^-33.
        ne.e = to_int(e.e, 2**-33)
        # Rate of inclination angle (semi-circle/sec). Scale factor 2-43. Range -8192...8191 (14 bits).
        ne.idot = to_int(e.idot, 2**-43)
        # Square root of semi-major axis (m). Scale factor 2^-19.
        ne.sqrt_a = to_int(e.sqrt_a, 2**-19)
        # Inclination angle at reference time (semi-circle). Scale factor 2^-31.
        ne.i0 = to_int(e.i0, 2**-31)
        # Longitude of ascending node at weekly epoch (semi-circle). Scale factor 2^-31.
        ne.omega0 = to_int(e.omega0, 2**-31)
        # Orbit radius, sine harmonic amplitude (m). Scale factor 2^-5.
        ne.crs = to_int(e.crs, 2**-5)
        # Inclination angle, sine harmonic amplitude (rad). Scale factor 2^-29.
        ne.cis = to_int(e.cis, 2**-29)
        # Argument of latitude, sine harmonic amplitude (rad). Scale factor 2^-29.
        ne.cus = to_int(e.cus, 2**-29)
        # Orbit radius, cosine harmonic amplitude (m). Scale factor 2^-5.
        ne.crc = to_int(e.crc, 2**-5)
        # Inclination angle, cosine harmonic amplitude (rad). Scale factor 2^-29.
        ne.cic = to_int(e.cic, 2**-29)
        # Argument of latitude, cosine harmonic amplitude (rad). Scale factor 2^-29.
        ne.cuc = to_int(e.cuc, 2**-29)

        return ne
