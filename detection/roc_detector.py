import numpy as np


class RateOfChangeDetector:
    def __init__(self, data):
        self.data = data
        self.window_size = 100

    def detect_decline(self):
        # Calculate the rate of change for each data point
        roc = np.diff(self.data)

        # Find the indices where the slope is negative
        negative_slope_indices = np.where(roc < 0)[0]

        # Apply a rolling window of size 100 and calculate the mean rate of change
        rolling_mean_roc = np.convolve(roc, np.ones(self.window_size), 'valid') / self.window_size

        # Find the index where the rate of change starts to decline
        decline_index = np.where(np.diff(rolling_mean_roc) < 0)[0]

        # Filter out the decline indices that correspond to positive slope
        valid_decline_indices = [index for index in decline_index if index in negative_slope_indices]

        return valid_decline_indices