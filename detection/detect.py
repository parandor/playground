
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema


class TroughDetector:
    def __init__(self, data):
        self.data = np.asarray(data)

    def detect_troughs(self):
        y_values = self.data[:, 1]
        trough_indices = argrelextrema(y_values, np.less)[0]
        return trough_indices

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
