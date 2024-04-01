from mic_sampler import MicSampler
from datetime import datetime
from struct import unpack

# Initialize ADS
sampler: MicSampler = MicSampler()

def clear_matrix():
    """Clear the led matrix"""
    return 0

def set_matrix():
    """Paint on the LED Matrix"""
    return 0

def convert_to_voltage(adc_value):
    """Convert raw ADC value to voltage based on reference voltage"""
    reference_voltage = 4.096 # change according to gain: https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/arduino-code#adjusting-gain
    return (adc_value / 32767) * reference_voltage

while True:
    fundamental_freq, low_freq_amp = sampler.capture()
