''' 
    Python based USB CLI Application interface control for vaunix LDA devices on windows-64bit machine
    JA 05/05/2021    Initial Verison of USB CLI control Interface
    (c) 2021-2022 by Vaunix Technology Corporation, all rights reserved
''' 
import os
from ctypes import cdll, c_int

__author__ = "Kazuma Moriuchi <kzm.moriuchi.ph@gmail.com"
__status__ = "production"
__version__ = "0.0.0"
__date__ = "2022/5/10"
__all__ = [
    "VaunixLDA133"
]


class VaunixLDA133:
    def __init__(self, serial_number):
        """establish communication with the LDA-133

        Parameters
        ----------
        serial_number : int
            serial number of LDA-133
        """
        self.vnx = cdll.LoadLibrary(
            "{0}\\VNX_atten64.dll".format(os.path.dirname(__file__))
        )
        self.vnx.fnLDA_SetTestMode(False)
        self.connect(serial_number=serial_number)

    def __del__(self):
        self.close()

    def connect(self, serial_number):
        """establish communication with the LDA-133

        Parameters
        ----------
        serial_number : int
            serial number of the LDA-133
        """
        DeviceIDArray = c_int * 20
        self.Devices = DeviceIDArray()
        self.numDevices = self.vnx.fnLDA_GetNumDevices()
        self.dev_info = self.vnx.fnLDA_GetDevInfo(self.Devices)
        self.devices_dict = {
            self.vnx.fnLDA_GetSerialNumber(self.Devices[index]): index
            for index in range(self.numDevices)
        }
        self.init_dev_dict = {}
        for index in range(self.numDevices):
            init_dev = self.vnx.fnLDA_InitDevice(self.Devices[index]) #initDeviceが超大事．これなかったらパラメータを設定できない．
        self.target_instrument = serial_number

    def close(self):
        """close communication with the LMS-133"""
        self.vnx.fnLDA_CloseDevice(
            self.Devices[self.devices_dict[self.target_instrument]]
        )

    def on(self):
        """set output state ON"""
        self.vnx.fnLDA_SetRFOn(
            self.Devices[self.devices_dict[self.target_instrument]], 1
        )

    def set_att(self, att):
        att = att * 4
        self.vnx.fnLDA_SetAttenuation(
            self.Devices[self.devices_dict[self.target_instrument]], int(att),
        )

    def get_att(self):
        return (
            self.vnx.fnLDA_GetAttenuation(
                self.Devices[self.devices_dict[self.target_instrument]]
            )
            / 4.0
        )
    
    def get_serial_number(self, devid):
        return (
            self.vnx.fnLDA_GetSerialNumber(
                self.Devices[self.devices_dict[self.target_instrument]]
            )
        )
        