# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# obscon-device.py - Alpaca API Device for Observingconditions - File Based
#
# Author:   Christopher Baker <netspec.inc _ at _ GMail> cb
#
# -----------------------------------------------------------------------------
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
#
# Edit History:
#    Concept based on Alpyca Device Example - rotatordevice.py
#
# 2023-07-29   cb   Initial edit
#

import datetime
import os

from threading import Timer
from threading import Lock
from logging import Logger
from config import Config

class ObservingConditionsDevice:
    """
    Observing Conditions read from a formatted text file.

    Debug tracing here via (commented out) print() to avoid locking issues.
    Hopefully you are familiar with Python threading and the need to lock shared data items.
    ** CB - I am not, but following giving example **

    """
    #
    # Only override __init_()  and run() (pydoc 17.1.2)
    # ** CB - Not sure I understand, keeping from example **
    #
    def __init__(self, logger: Logger):
        # Initialize the last read time and obscond_data as None
        self._last_file_read_time = None
        self._obscond_data = None
        #self.file_path = 'C:\\Users\\LocalAdmin\\Desktop\\test\\sageweatherdata.txt'  # Replace with the actual file path
        self.file_path = Config.weather_data_file
        # ..................
        self._lock = Lock()
        self.name: str = 'device'
        self.logger = logger
        #
        # Observing Conditions Constants
        # ** CB - Commenting out for now, May add back my own for ObsCond later
        #
        #self._can_reverse: bool = True
        #self._step_size: float = 1.0
        #self._steps_per_sec: int = 6
        #
        # Rotator device state variables
        # ** CB - Commenting out for now, May add back my own for ObsCond later
        #
        #self._reverse = False
        #self._mech_pos = 0.0
        #self._tgt_mech_pos = 0.0
        #self._pos_offset = 0.0      # TODO In real life this must be persisted
        #self._is_moving = False
        #self._connected = False
        #
        # Rotator engine
        # ** CB - Commenting out for now, might be necessary to see how often to read file
        #
        #self._timer: Timer = None
        #self._interval: float = 1.0 / self._steps_per_sec
        #self._stopped: bool = True

    @property
    def connected(self) -> bool:
        self.logger.debug('[entering connected]')
        self._lock.acquire()
        res = self._connected
        self._lock.release()
        
        # Get the obscond_data
        obscond_data = self._get_obscond_data()

        # Do something with the obscond_data here (replace the print statement with your desired logic)
        self.logger.debug(f'[connected] ObsCond Data: {obscond_data}')

        return res
    
    @connected.setter
    def connected (self, connected: bool):
        self._lock.acquire()
        self._connected = connected
        self._lock.release()
        if connected:
            self.logger.debug('[connected]')
        else:
            self.logger.debug('[disconnected]')

    @property
    def readobscondfile(self):
        # Check if the obscond_data is cached and if it's still valid
        if self._obscond_data and not self._is_cached_file_data_old(self._last_file_read_time):
            return self._obscond_data

        # Check if the file is present and if it's been more than 5 minutes since the last read
        # obscondfilelastread = self._get_last_file_read_time()  # Replace this with your own method to get the last read time

        # Check if the file exists and the last read time condition is met
        #if os.path.exists(self.file_path) and not self._is_cached_file_data_old(obscondfilelastread):
        if os.path.exists(self.file_path):
            self.logger.debug(f'[ObservingConditionsDevice.readobscondfile: file_path: {self.file_path}]')
            with open(self.file_path, 'r') as file:
                self.logger.debug(f'[ObservingConditionsDevice.readobscondfile: Reading file]')
                obscond_data = {}
                line = file.readline()
                if line.strip():
                    data_values = line.strip().split()
                    keys = ["FileWriteDate", "FileWriteTime", "TempScale", "WindSpeedScale", "SkyTemp", "AmbientTemp",
                            "SensorTemp", "WindSpeed", "Humidity", "DewPoint", "DewHeaterPrcnt", "RainFlag", "WetFlag",
                            "ElapsedTimeLastFileWrite", "ElapsedDaysLastFileWrite", "CloudFlag", "WindFlag", "RainFlag2",
                            "DarknessFlag", "RoofClosedFlag", "SafeFlag"]
                    for i in range(min(len(keys), len(data_values))):
                        obscond_data[keys[i]] = data_values[i]

                # Update the last read time and cache the obscond_data
                #self._update_last_file_read_time(datetime.datetime.now())
                self._last_file_read_time = datetime.datetime.now()
                self._obscond_data = obscond_data

            return self._obscond_data

        # If the file is not present or the last read time condition is not met, return the cached obscond_data
        return self._obscond_data

    #
    # Methods
    # TODO - This is supposed to throw if the final position is outside 0-360, but WHICH position? Mech or user????
    #

    def Halt(self) -> None:
        self.logger.debug('[Halt]')
        self.stop()
 
     # Helper method to get the obscond_data from the readobscondfile property
    def _get_obscond_data(self):
        # Call the readobscondfile property to get the obscond_data
        return self.readobscondfile
    
    # Helper method to check if the cached file data has expired
    def _is_cached_file_data_old(self, datetime_value):
        if datetime_value:
            timeout = Config.weather_data_cache_timeout # Timeout value from config.toml - INT
            if timeout < 60:
                timeout=60 # Force min cache data to 60
            now = datetime.datetime.now()
            time_difference = now - datetime_value
            self.logger.debug(f'[ObservingConditionsDevice._is_cached_file_data_old: Timeout Set to: {str(timeout)} Time Difference: {str(time_difference.total_seconds())}]')
            return time_difference.total_seconds() > timeout  # User Set - Must be at least 60 sec
        return True

    # Replace these placeholder methods with your actual implementations to get and update the last read time
    def _get_last_file_read_time(self):
        # Replace this with your own method to get the last read time from somewhere (e.g., a class attribute or file)
        return self._last_file_read_time

    def _update_last_file_read_time(self, datetime_value):
        # Replace this with your own method to update the last read time (e.g., save to a class attribute or file)
        self._last_file_read_time = datetime_value


        
class SensorOptionalFunct:
    # Define the sensor's optional capabilities
    sensor_functions = {
        "CloudCover": Config.sensor_cloud_avail,
        "DewPoint": Config.sensor_dew_avail,
        "Humidity": Config.sensor_dew_avail,
        "Pressure": Config.sensor_pres_avail,
        "RainRate": Config.sensor_rain_avail,
        "SkyBrightness": Config.sensor_skyb_avail,
        "SkyQuality": Config.sensor_skyq_avail,
        "SkyTemperature": Config.sensor_skyt_avail,
        "StarFWHM": Config.sensor_star_avail,
        "Temperature": Config.sensor_temp_avail,
        "WindDirection": Config.sensor_windd_avail,
        "WindGust": Config.sensor_windg_avail,
        "WindSpeed": Config.sensor_winds_avail,
    }
    
    sensor_descriptions = {
         "CloudCover": Config.sensor_cloud_desc,
        "DewPoint": Config.sensor_dew_desc,
        "Humidity": Config.sensor_hum_desc,
        "Pressure": Config.sensor_pres_desc,
        "RainRate": Config.sensor_rain_desc,
        "SkyBrightness": Config.sensor_skyb_desc,
        "SkyQuality": Config.sensor_skyq_desc,
        "SkyTemperature": Config.sensor_skyt_desc,
        "StarFWHM": Config.sensor_star_desc,
        "Temperature": Config.sensor_temp_desc,
        "WindDirection": Config.sensor_windd_desc,
        "WindGust": Config.sensor_windg_desc,
        "WindSpeed": Config.sensor_winds_desc,
       
    }