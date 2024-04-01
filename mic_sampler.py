# Reference: https://github.com/scarey/bass-reactive-leds/blob/main/audio_handler.py
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from ulab import numpy as np
from ulab import utils as utils
import board
import busio

NUM_SAMPLES = 256
REACT_CROSSOVER = 400
ADS_GAIN = 1

class MicSampler:
    """Sampler :O"""
    def __init__(self, num_samples: int = NUM_SAMPLES, crossover: int = REACT_CROSSOVER):
        # Initialize ADS1115
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.num_samples = num_samples
        self.crossover = crossover
        self.samples = []

    def capture(self):
        """Capture samples"""
        sample_start = time.ticks_us()

        for _ in range(self.num_samples):
            self.samples.append(AnalogIn(self.ads, ADS.P2).value)

        sample_duration = time.ticks_diff(time.ticks_us(), sample_start) / 1_000_000
        array = np.array(self.samples)
        self.samples.clear()

        # split into frequency buckets
        output = utils.spectrogram(array)
        max_magnitude = 0
        max_low_freq_mag = 0
        fundamental_freq = 0

        for i in range(1, int(self.num_samples / 2) + 1):
            mag = output[i]
            freq = i * 1.0 / sample_secs

            if mag > max_magnitude:
                fundamental_freq = freq
                max_magnitude = mag
            if freq < self.crossover and mag > max_low_freq_mag:
                max_low_freq_mag = mag

            print("Freq: {}, Low Mag: {}".format(freq, max_low_freq_mag))

        low_freq_amp = max_low_freq_mag * 2 / self.num_samples

        return fundamental_freq, low_freq_amp
