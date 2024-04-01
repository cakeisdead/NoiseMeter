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

def calculate_levels(data, chunk,sample_rate):
    print("Calculating levels")
    print(f"Data: {data}")
    # Convert raw data to numpy array
    #data = unpack("%dh"%(len(data)/2),data)
    #data = np.array(data, dtype='h')
    # Apply FFT - real data so rfft used
    fourier = np.fft.rfft(data)
    print(fourier)
    # Remove last element in array to make it the same size as chunk
    fourier = np.delete(fourier,len(fourier)-1)
    # Find amplitude
    power = np.log10(np.abs(fourier))**2
    # Arrange array into 8 rows for the 8 bars on LED matrix
    power = np.reshape(power,(8,chunk/8))
    matrix = np.int_(np.average(power,axis=1)/4)
    return matrix

while True:
    sample_start = datetime.now()
    SAMPLE_STATUS = True
    SIGNAL_MAX = 0
    SIGNAL_MIN = MAX_RES
    AVG_P2P = 1

    while SAMPLE_STATUS is True:
        channel = AnalogIn(ads, ADS.P2)
        sample = channel.value

        if sample < MAX_RES:
            if sample > SIGNAL_MAX:
                SIGNAL_MAX = sample
            elif sample < SIGNAL_MIN:
                SIGNAL_MIN = sample

        elapsed = (datetime.now()-sample_start).total_seconds()*1000
        SAMPLE_STATUS = elapsed <= SAMPLE_SIZE
    
    peak_to_peak = SIGNAL_MAX - SIGNAL_MIN
    #AVG_P2P = (peak_to_peak + AVG_P2P) / 2
    #print(AVG_P2P)
    voltage = convert_to_voltage(peak_to_peak)
    #print(voltage)

    try:
        matrix = calculate_levels(voltage, CHUNKS, MAX_RES)
        print(matrix)
    except:
        pass

