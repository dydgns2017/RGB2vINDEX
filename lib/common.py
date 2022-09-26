import numpy as np

def result_histogram(result):
    np_2d = np.ndarray(
        buffer=result.write_to_memory(),
        dtype=np.float32,
        shape=[result.height, result.width]
    )

    flat_result = np_2d.flatten()

    histogram = np.histogram(flat_result, bins=256)[0]
    return histogram

def math_map_value(value, in_low, in_high, to_low, to_high):
    return to_low + (value - in_low) * (to_high - to_low) / (in_high - in_low)

def find_clipped_min_max(histogram, nmin, nmax):
    # histogram
    summed = sum(histogram)
    three_percent = summed * 0.03
    lower_sum = 0
    upper_sum = 0
    last_lower_i = 0
    last_upper_i = 0
    histogram_len = len(histogram)
    for i in range(histogram_len):
    # summing up values in lower_sum til the sum is >= 3% of the sum of all data values
    # last_lower_i will be the data position right before lower_sum summed equal to 3% of the sum of all data values
        if lower_sum < three_percent:
            lower_sum += histogram[i]
            last_lower_i = i
        # // the same with last_upper_i
        if upper_sum < three_percent:
            upper_sum += histogram[histogram_len - 1 - i]
            last_upper_i = histogram_len - 1 - i
    return {
    'nmin': math_map_value(last_lower_i, 0, 255, nmin, nmax),
    'nmax': math_map_value(last_upper_i, 0, 255, nmin, nmax)
    }