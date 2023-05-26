from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage.filters import uniform_filter1d

class TroughDetector:
    def __init__(self, data, discretization_factor=1000, smoothing_window=3, peak_prominence=1000, peak_distance=5, peak_height=-12000, peak_width=None):
        self.data = np.asarray(data)
        self.discretization_factor = discretization_factor
        self.smoothing_window = smoothing_window
        self.peak_prominence = peak_prominence
        self.peak_distance = peak_distance
        self.peak_height = peak_height
        self.peak_width = peak_width

    def detect_troughs(self):
        discretized_data = self.discretize_data()
        smoothed_data = self.get_smoothed_data(discretized_data)
        neg_smoothed_data = -smoothed_data
        peak_indices, _ = find_peaks(neg_smoothed_data, prominence=self.peak_prominence, height=self.peak_height, width=self.peak_width, distance=self.peak_distance)
        return peak_indices

    def discretize_data(self):
        y_values = self.data[:, 1]
        discretized_data = np.round(y_values * self.discretization_factor)
        return discretized_data

    def get_smoothed_data(self, data):
        smoothed_data = uniform_filter1d(data, size=self.smoothing_window, mode='reflect')
        return smoothed_data

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
