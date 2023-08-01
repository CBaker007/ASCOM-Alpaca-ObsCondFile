# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# conf.py - Device configuration file and shared logger construction
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# GitHub: https://github.com/ASCOMInitiative/AlpycaDevice
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 More config items, separate logging section
# 27-Dec-2022   rbd 0.1 Move shared logger construction and global
#               var here. MIT license and module header. No mcast.
#
import sys
import toml
import logging

#
# This slimy hack is for Sphinx which, despite the toml.load() being
# run only once on the first import, it can't deal with _dict not being
# initialized or ?!?!?!?!? If you try to use getcwd() in the file name
# here, it will also choke Sphinx. This cost me a day.
#
_dict = {}
_dict = toml.load(f'{sys.path[0]}/config.toml')    # Errors here are fatal.
def get_toml(sect: str, item: str):
    if not _dict is {}:
        return _dict[sect][item]
    else:
        return ''

class Config:
    """Device configuration in ``config.toml``"""
    # ---------------
    # Network Section
    # ---------------
    ip_address: str = get_toml('network', 'ip_address')
    port: int = get_toml('network', 'port')
    # --------------
    # Server Section
    # --------------
    location: str = get_toml('server', 'location')
    verbose_driver_exceptions: bool = get_toml('server', 'verbose_driver_exceptions')
    # --------------
    # Device Section
    # --------------
    weather_data_file: str = get_toml('device', 'weather_data_file')
    weather_data_cache_timeout: int = get_toml('device', 'weather_data_cache_timeout')
    sensor_cloud_avail: bool = get_toml('device', 'sensor_cloud_avail')
    sensor_dew_avail: bool = get_toml('device', 'sensor_dew_avail')        # Also used for humity because both required to be same
    sensor_hum_avail: bool = get_toml('device', 'sensor_dew_avail')
    sensor_pres_avail: bool = get_toml('device', 'sensor_pres_avail')
    sensor_rain_avail: bool = get_toml('device', 'sensor_rain_avail')
    sensor_skyb_avail: bool = get_toml('device', 'sensor_skyb_avail')
    sensor_skyq_avail: bool = get_toml('device', 'sensor_skyq_avail')
    sensor_skyt_avail: bool = get_toml('device', 'sensor_skyt_avail')
    sensor_star_avail: bool = get_toml('device', 'sensor_star_avail')
    sensor_temp_avail: bool = get_toml('device', 'sensor_temp_avail')
    sensor_windd_avail: bool = get_toml('device', 'sensor_windd_avail')
    sensor_windg_avail: bool = get_toml('device', 'sensor_windg_avail')
    sensor_winds_avail: bool = get_toml('device', 'sensor_winds_avail')
    sensor_cloud_desc: str = get_toml('device', 'sensor_cloud_desc')
    sensor_dew_desc: str = get_toml('device', 'sensor_dew_desc')
    sensor_hum_desc: str = get_toml('device', 'sensor_hum_desc')
    sensor_pres_desc: str = get_toml('device', 'sensor_pres_desc')
    sensor_rain_desc: str = get_toml('device', 'sensor_rain_desc')
    sensor_skyb_desc: str = get_toml('device', 'sensor_skyb_desc')
    sensor_skyq_desc: str = get_toml('device', 'sensor_skyq_desc')
    sensor_skyt_desc: str = get_toml('device', 'sensor_skyt_desc')
    sensor_star_desc: str = get_toml('device', 'sensor_star_desc')
    sensor_temp_desc: str = get_toml('device', 'sensor_temp_desc')
    sensor_windd_desc: str = get_toml('device', 'sensor_windd_desc')
    sensor_windg_desc: str = get_toml('device', 'sensor_windg_desc')
    sensor_winds_desc: str = get_toml('device', 'sensor_winds_desc')
    # ---------------
    # Logging Section
    # ---------------
    log_filename: str = get_toml('logging', 'log_filename') #ADDED by CB
    log_level: int = logging.getLevelName(get_toml('logging', 'log_level'))  # Not documented but works (!!!!)
    log_to_stdout: str = get_toml('logging', 'log_to_stdout')
    max_size_mb: int = get_toml('logging', 'max_size_mb')
    num_keep_logs: int = get_toml('logging', 'num_keep_logs')

