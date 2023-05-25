from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage.filters import uniform_filter1d


class TroughDetector:
    def __init__(self, data, range_size=5, smoothing_window=3):
        self.data = np.asarray(data)
        self.range_size = range_size
        self.smoothing_window = smoothing_window

    def detect_troughs(self):
        y_values = self.data[:, 1]
        smoothed_data = uniform_filter1d(
            y_values, size=self.smoothing_window, mode='reflect')
        trough_indices = argrelextrema(
            smoothed_data, np.less, order=self.range_size)[0]
        return trough_indices

    def is_trough_detected(self):
        trough_indices = self.detect_troughs()
        return len(trough_indices) > 0

    def plot_troughs(self, trough_indices):
        x_values = self.data[:, 0]
        y_values = self.data[:, 1]

        plt.plot(x_values, y_values)
        plt.scatter(x_values[trough_indices],
                    y_values[trough_indices], c='r', label='Troughs')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Trough Detection')
        plt.legend()
        plt.show()
