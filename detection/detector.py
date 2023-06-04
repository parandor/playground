import numpy as np
from scipy.signal import find_peaks
from detection.plotter import Plotter
from detection.filter import Filter
from data.convert import Converter

class TroughDetector:
    def __init__(self, data, discretization_factor=1000, smoothing_window=7, peak_prominence=500, peak_distance=None, peak_height=-30000, peak_width=None):
        self.data = np.asarray(data)
        self.peak_prominence = peak_prominence
        self.peak_distance = peak_distance
        self.peak_height = peak_height
        self.peak_width = peak_width
        self.peak_indices = None
        self.filter = Filter(discretization_factor, smoothing_window)
        self.label = "Trough"

    def detect_troughs(self):
        # Run filter pipeline first prior to detection
        self.filter.discretize_data(self.data)
        self.filter.smoothe_data(self.filter.discretized_data)
        filtered_data = self.filter.remove_outliers(self.filter.smoothed_data)
        neg_filtered_data = -filtered_data
        self.peak_indices, _ = find_peaks(neg_filtered_data, prominence=self.peak_prominence, height=self.peak_height, width=self.peak_width, distance=self.peak_distance)

    def get_troughs(self):
        return self.peak_indices

    def is_trough_detected(self):
        return len(self.peak_indices) > 0

    def plot_troughs_raw(self):
        Plotter.plot_events(self.data, self.peak_indices, self.label)

    def plot_troughs_smoothed(self):
        Plotter.plot_events(Converter.to_col_stack(self.filter.smoothed_data), self.peak_indices, self.label)

    def plot_troughs_filtered(self):
        Plotter.plot_events(Converter.to_col_stack(self.filter.filtered_data), self.peak_indices, self.label)
