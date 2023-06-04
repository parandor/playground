import numpy as np
from scipy.ndimage.filters import uniform_filter1d

class Filter:
    def __init__(self, discretization_factor=1000, smoothing_window=7):
        self.discretization_factor = discretization_factor
        self.smoothing_window = smoothing_window
        self.discretized_data = None
        self.smoothed_data = None
        self.filtered_data = None

    def discretize_data(self, data):
        y_values = data[:, 1]
        self.discretized_data = np.round(y_values * self.discretization_factor)
        return self.discretized_data

    def smoothe_data(self, data):
        self.smoothed_data = uniform_filter1d(data, size=self.smoothing_window, mode='reflect')
        return self.smoothed_data

    def remove_outliers(self, data, threshold=3.5):
        # todo: should we smoothe twice?
        smoothed_data = self.smoothe_data(data)
        diff = np.abs(smoothed_data[1:] - smoothed_data[:-1])
        if len(diff) < 2:
            return data
        median_diff = np.median(diff)
        mad = np.median(np.abs(diff - median_diff))
        
        if mad == 0:
            return data
        
        z_scores = 0.6745 * (diff - median_diff) / mad
        outliers = np.where(np.abs(z_scores) > threshold)[0]
        
        self.filtered_data = np.copy(data)
        for idx in outliers:
            if idx > 0 and idx < len(self.filtered_data) - 2:
                # Replace outlier with average
                self.filtered_data[idx] = (self.filtered_data[idx] - 1 + self.filtered_data[idx + 1]) / 2  
        
        return self.filtered_data