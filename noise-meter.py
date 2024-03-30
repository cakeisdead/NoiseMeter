import board
import numpy as np
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
from struct import unpack

# Initialize ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Settings
SAMPLE_SIZE = 50
MAX_RES = 44100
CHUNKS = 512
ads.gain = 1

def ClearMatrix():
	'''Clear the led matrix'''

def SetMatrix():
	'''Paint data on the led matrix'''

def calculate_levels(data, chunk,sample_rate):
	# Convert raw data to numpy array
	data = unpack("%dh"%(len(data)/2),data)
	data = np.array(data, dtype='h')
	# Apply FFT - real data so rfft used
	fourier=np.fft.rfft(data)
	# Remove last element in array to make it the same size as chunk
	fourier=np.delete(fourier,len(fourier)-1)
	# Find amplitude
	power = np.log10(np.abs(fourier))**2
	# Araange array into 8 rows for the 8 bars on LED matrix
	power = np.reshape(power,(8,chunk/8))
	matrix= np.int_(np.average(power,axis=1)/4)
	return matrix

while True:
	sample_start = datetime.now()
	SAMPLE_STATUS = True
	signal_max = 0
	signal_min = MAX_RES
	avg_p2p = 1

	while SAMPLE_STATUS is True:
		channel = AnalogIn(ads, ADS.P2)
		sample = channel.value

		if sample < MAX_RES:
			if sample > signal_max:
				signal_max = sample
			elif sample < signal_min:
				signal_min = sample

		elapsed = (datetime.now()-sample_start).total_seconds()*1000
		SAMPLE_STATUS = elapsed <= SAMPLE_SIZE
	peak_to_peak = signal_max - signal_min
	avg_p2p = (peak_to_peak + avg_p2p) / 2

	try:
		matrix = calculate_levels(avg_p2p, CHUNKS, MAX_RES)
		print(matrix)
