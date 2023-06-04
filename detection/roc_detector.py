import numpy as np
from detection.plotter import Plotter
from detection.filter import Filter
from data.convert import Converter

class RateOfChangeDetector:
    def __init__(self, data, window_size=500, discretization_factor=1000, smoothing_window=7):
        self.data = data
        self.window_size = window_size
        self.filter = Filter(discretization_factor, smoothing_window)
        self.decline_indices = None

    def detect_decline(self, min_threshold, max_threshold):
        # Run filter pipeline first prior to detection
        self.filter.discretize_data(self.data)
        self.filter.smoothe_data(self.filter.discretized_data)
        filtered_data = self.filter.remove_outliers(self.filter.smoothed_data)
        roc = np.diff(filtered_data)
        negative_slope_indices = np.where(roc < 0)[0]
        rolling_mean_roc = np.convolve(roc, np.ones(self.window_size), 'valid') / self.window_size
        decline_index = np.where(np.diff(rolling_mean_roc) < 0)[0]
        valid_decline_indices = []

        for index in decline_index:
            if index in negative_slope_indices:
                rate_of_change = roc[index]
                if min_threshold <= rate_of_change <= max_threshold:
                    valid_decline_indices.append(index)

        self.decline_indices = valid_decline_indices
        return self.decline_indices

    def plot_decline_raw(self):
        Plotter.plot_events(self.data, self.decline_indices, "Decline")

    def plot_decline_filtered(self):
        Plotter.plot_events(Converter.to_col_stack(self.filter.filtered_data), self.decline_indices, "Decline")
