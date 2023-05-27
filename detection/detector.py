from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.ndimage.filters import uniform_filter1d

class TroughDetector:
    def __init__(self, data, discretization_factor=1000, smoothing_window=7, peak_prominence=500, peak_distance=None, peak_height=-30000, peak_width=None):
        self.data = np.asarray(data)
        self.discretization_factor = discretization_factor
        self.smoothing_window = smoothing_window
        self.peak_prominence = peak_prominence
        self.peak_distance = peak_distance
        self.peak_height = peak_height
        self.peak_width = peak_width
        self.peak_indices = None
        self.filtered_data = None

    def detect_troughs(self):
        discretized_data = self.discretize_data()
        smoothed_data = self.get_smoothed_data(discretized_data)
        self.filtered_data = self.remove_outliers(smoothed_data)
        neg_filtered_data = -self.filtered_data
        self.peak_indices, _ = find_peaks(neg_filtered_data, prominence=self.peak_prominence, height=self.peak_height, width=self.peak_width, distance=self.peak_distance)

    def get_troughs(self):
        return self.peak_indices
    
    def get_filtered_data(self):
        return self.filtered_data

    def discretize_data(self):
        y_values = self.data[:, 1]
        discretized_data = np.round(y_values * self.discretization_factor)
        return discretized_data

    def get_smoothed_data(self, data):
        smoothed_data = uniform_filter1d(data, size=self.smoothing_window, mode='reflect')
        return smoothed_data

    def remove_outliers(self, data, threshold=3.5):
        smoothed_data = self.get_smoothed_data(data)
        diff = np.abs(smoothed_data[1:] - smoothed_data[:-1])
        median_diff = np.median(diff)
        mad = np.median(np.abs(diff - median_diff))
        z_scores = 0.6745 * (diff - median_diff) / mad
        outliers = np.where(np.abs(z_scores) > threshold)[0]
        filtered_data = np.copy(data)
        filtered_data[outliers+1] = np.nan
        return filtered_data

    def is_trough_detected(self):
        return len(self.peak_indices) > 0

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
