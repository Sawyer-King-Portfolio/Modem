import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 48000
BAUD = 300

SAMPLES_PER_BIT = SAMPLE_RATE // BAUD

BITS_PER_BYTE = 10
SAMPLES_PER_BYTE = SAMPLES_PER_BIT * BITS_PER_BYTE

FREQ_0 = 2025
FREQ_1 = 2225

def tone_power(section, freq, sample_rate):
    """
    Used to measure how much a section matches a frequency.
    """

    indices = np.arange(len(section))
    time = indices / sample_rate

    precomputed_cos = np.cos(2 * np.pi * freq * time)
    precomputed_sin = np.sin(2 * np.pi * freq * time)

    cos_align = np.dot(section, precomputed_cos)
    sin_align = np.dot(section, precomputed_sin)

    return cos_align * cos_align + sin_align * sin_align

def bit_decoder(section, sample_rate):
    """
    Used to determine which frequency a bit aligns with.
    """

    power_0 = tone_power(section, FREQ_0, sample_rate)
    power_1 = tone_power(section, FREQ_1, sample_rate)

    return 1 if power_1 > power_0 else 0

def byte_decoder(bits):
    """
    Used to parse 10 bits at a time based on a start bit, end bit, and the bits between which contain the data.
    """
    
    start_bit = bits[0]
    end_bit = bits[9]
    between_bits = bits[1:9]

    if start_bit != 0:
        print("Bad start bit")

    if end_bit != 1:
        print("Bad end bit")

    value = 0
    for i, bit in enumerate(between_bits):
        value += bit << i

    return value

def main():
    sample_rate, samples = wavfile.read("message.wav")

    samples = samples.astype(np.float32) / 32768.0

    num_bits = len(samples) // SAMPLES_PER_BIT
    bits = []

    for i in range(num_bits):
        start_bit = i * SAMPLES_PER_BIT
        end_bit = start_bit + SAMPLES_PER_BIT
        section = samples[start_bit:end_bit]

        bit = bit_decoder(section, sample_rate)
        bits.append(bit)

    chars = []

    for i in range(0, len(bits) - BITS_PER_BYTE + 1, BITS_PER_BYTE):
        byte_bits = bits[i:i + BITS_PER_BYTE]
        byte_value = byte_decoder(byte_bits)

        chars.append(chr(byte_value))

    message = "".join(chars)

    print("Message:",message)

    with open("message.txt", "w", encoding="utf-8") as f:
        f.write(message)

if __name__ == "__main__":
    main()