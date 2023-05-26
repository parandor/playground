from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage.filters import uniform_filter1d

class TroughDetector:
    def __init__(self, data, range_size=3, smoothing_window=3, discretization_factor=1):
        self.data = np.asarray(data)
        self.range_size = range_size
        self.smoothing_window = smoothing_window
        self.discretization_factor = discretization_factor
        
    def detect_troughs(self):
        smoothed_data = self.get_smoothed_data()
        trough_indices = argrelextrema(
            smoothed_data, np.less, order=self.range_size)[0]
        return trough_indices

    def is_trough_detected(self):
        trough_indices = self.detect_troughs()
        return len(trough_indices) > 0

    def get_smoothed_data(self):
        smoothed_data = uniform_filter1d(
            self.discretize_data(), size=self.smoothing_window, mode='reflect')
        return smoothed_data
    
    def discretize_data(self):
        y_values = self.data[:, 1]
        discretized_data = np.round(y_values * self.discretization_factor)
        return discretized_data

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
