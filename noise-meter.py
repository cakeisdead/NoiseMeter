import board
import numpy as np
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

SAMPLE_SIZE = 50
MAX_RES = 440000
ads.gain = 1

while True:
	sample_start = datetime.now()
	sample_status = True
	signal_max = 0
	signal_min = MAX_RES
	avg_p2p = 1

	while sample_status == True:
		chan = AnalogIn(ads, ADS.P2)
		sample = chan.value

		if (sample < MAX_RES):
			if (sample > signal_max):
				signal_max = sample
			elif (sample < signal_min):
				signal_min = sample

		elapsed = (datetime.now()-sample_start).total_seconds()*1000
		sample_status = elapsed <= SAMPLE_SIZE

	peak_to_peak = signal_max - signal_min
	avg_p2p = (peak_to_peak + avg_p2p) / 2
	visual = int(avg_p2p % 1)
	print(avg_p2p) 
