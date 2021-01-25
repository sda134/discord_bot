#!/usr/bin/env python3
#coding: UTF-8

import sys
import time
import spidev
import binascii
from enum import IntEnum

class Bme280Mode(IntEnum):
    SLEEP = 0b00
    FORCED = 0b01	# or 0b10
    NORMAL = 0b11
    
class Bme280(): 
	def __init__(self):
		self.mode = Bme280Mode.SLEEP
		self.osrs_t = 0b001
		self.osrs_p = 0b001
		self.osrs_h = 0b001
		self._digT = []
		self._digP = []
		self._digH = []
		self._spi = spidev.SpiDev()
	
	def __del__(self):
		self._spi.close()

	def open(self):
		# spi setup
		self._spi.open(0, 0)
		self._spi.max_speed_hz = 100000

		# setup
		ctrl_meas = (self.osrs_t << 5) | (self.osrs_p << 2) | self.mode
		ctrl_hum = self.osrs_h		
		self._spi.xfer([0x74,ctrl_meas, 0x72,ctrl_hum])	# addr 0xF4 addr 0xF2

		# get calibration data
		self._get_calib_param()

		
	def close(self):
		pass

	def get_data(self):
		# get_raw_data
		data = self._read_bytes(0xF7, 8)
		press_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
		temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
		humid_raw  = (data[6] << 8)  |  data[7]
				
		# compensation must be in this order
		temp = self._compensate_T(temp_raw)/ 5120.0
		press = self._compensate_P(press_raw) / 100
		humid = self._compensate_H(humid_raw)			

		return [press, temp, humid]


	
	# private methods
	def _read_bytes(self, address, byte_count):
		adr = 0x80 | address
		data_list = [adr]
		while len(data_list) <= byte_count:
			data_list.append(0x00)
		ret = self._spi.xfer2(data_list)
		return bytearray(ret[1:])

	def _write_byte(self, address, data_byte):
		adr = address & 0x7F
		return self._spi.xfer2([adr,data_byte])
		
	def _get_calib_param(self):
		calib = []
		calib.extend(self._read_bytes(0x88, 25))
		calib.extend(self._read_bytes(0xE1, 7))

		self._digT.append((calib[1] << 8) | calib[0])
		self._digT.append((calib[3] << 8) | calib[2])
		self._digT.append((calib[5] << 8) | calib[4])
		self._digP.append((calib[7] << 8) | calib[6])
		self._digP.append((calib[9] << 8) | calib[8])
		self._digP.append((calib[11]<< 8) | calib[10])
		self._digP.append((calib[13]<< 8) | calib[12])
		self._digP.append((calib[15]<< 8) | calib[14])
		self._digP.append((calib[17]<< 8) | calib[16])
		self._digP.append((calib[19]<< 8) | calib[18])
		self._digP.append((calib[21]<< 8) | calib[20])
		self._digP.append((calib[23]<< 8) | calib[22])
		self._digH.append( calib[24] )
		self._digH.append((calib[26]<< 8) | calib[25])
		self._digH.append( calib[27] )
		self._digH.append((calib[28]<< 4) | (0x0F & calib[29]))
		self._digH.append((calib[30]<< 4) | ((calib[29] >> 4) & 0x0F))
		self._digH.append( calib[31] )
		
		for i in range(1,2):
			if self._digT[i] & 0x8000:
				self._digT[i] = (-self._digT[i] ^ 0xFFFF) + 1

		for i in range(1,8):
			if self._digP[i] & 0x8000:
				self._digP[i] = (-self._digP[i] ^ 0xFFFF) + 1

		for i in range(0,6):
			if self._digH[i] & 0x8000:
				self._digH[i] = (-self._digH[i] ^ 0xFFFF) + 1  
				


	def _compensate_P(self, adc_P):
		global  t_fine
		pressure = 0.0
		
		v1 = (t_fine / 2.0) - 64000.0
		v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self._digP[5]
		v2 = v2 + ((v1 * self._digP[4]) * 2.0)
		v2 = (v2 / 4.0) + (self._digP[3] * 65536.0)
		v1 = (((self._digP[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8)  + ((self._digP[1] * v1) / 2.0)) / 262144
		v1 = ((32768 + v1) * self._digP[0]) / 32768
		
		if v1 == 0:
			return 0
		pressure = ((1048576 - adc_P) - (v2 / 4096)) * 3125
		if pressure < 0x80000000:
			pressure = (pressure * 2.0) / v1
		else:
			pressure = (pressure / v1) * 2
		v1 = (self._digP[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
		v2 = ((pressure / 4.0) * self._digP[7]) / 8192.0
		pressure = pressure + ((v1 + v2 + self._digP[6]) / 16.0)  
		return pressure

	def _compensate_T(self, adc_T):
		global t_fine
		v1 = (adc_T / 16384.0 - self._digT[0] / 1024.0) * self._digT[1]
		v2 = (adc_T / 131072.0 - self._digT[0] / 8192.0) * (adc_T / 131072.0 - self._digT[0] / 8192.0) * self._digT[2]
		t_fine = v1 + v2
		temperature = t_fine
		return temperature

	def _compensate_H(self, adc_H):
		global t_fine
		var_h = t_fine - 76800.0
		if var_h != 0:
			var_h = (adc_H - (self._digH[3] * 64.0 + self._digH[4]/16384.0 * var_h)) * (self._digH[1] / 65536.0 * (1.0 + self._digH[5] / 67108864.0 * var_h * (1.0 + self._digH[2] / 67108864.0 * var_h)))
		else:
			return 0
		var_h = var_h * (1.0 - self._digH[0] * var_h / 524288.0)
		if var_h > 100.0:
			var_h = 100.0
		elif var_h < 0.0:
			var_h = 0.0
		return var_h		

