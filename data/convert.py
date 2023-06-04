import numpy as np

class Converter:
    @staticmethod
    def to_col_stack_with_mean(data):
        points = list(data)

        y_values_temp = [point['mean'] for point in points if point['mean'] is not None]
        x_indices = np.arange(len(y_values_temp))
        y_values = np.array(y_values_temp)

        return np.column_stack((x_indices, y_values))
    
    @staticmethod
    def to_col_stack(data):
        y_values = np.array(list(data))
        x_indices = np.arange(len(y_values))
        return np.column_stack((x_indices, y_values))

    