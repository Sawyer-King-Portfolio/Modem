import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 48000
BAUD = 300

SAMPLES_PER_BIT = SAMPLE_RATE // BAUD

FREQ_0 = 2025
FREQ_1 = 2225

def tone_power(section, freq, sample_rate):

    indices = np.arange(len(section))
    time = indices / sample_rate

    precomputed_cos = np.cos(2 * np.pi * freq * time)
    precomputed_sin = np.sin(2 * np.pi * freq * time)

    cos_align = np.dot(section, precomputed_cos)
    sin_align = np.dot(section, precomputed_sin)

    return cos_align * cos_align + sin_align * sin_align

def bit_decoder(section, sample_rate):
    print(section)
    print(sample_rate)

    power_0 = tone_power(section, FREQ_0, sample_rate)
    power_1 = tone_power(section, FREQ_1, sample_rate)

    return 1 if power_1 > power_0 else 0

def main():
    sample_rate, samples = wavfile.read("message.wav")

    print(sample_rate)
    print(samples)

    num_bits = len(samples) // SAMPLES_PER_BIT
    bits = []

    for i in range(num_bits):
        start_bit = i * SAMPLES_PER_BIT
        end_bit = start_bit + SAMPLES_PER_BIT
        section = samples[start_bit:end_bit]

        bit = bit_decoder(section, sample_rate)
        print(bit)

if __name__ == "__main__":
    main()