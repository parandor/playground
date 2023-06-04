import numpy as np

class Converter:
    @staticmethod
    def to_column_stack(result):
        points = list(result)

        y_values_temp = [point['mean'] for point in points if point['mean'] is not None]
        x_indices = np.arange(len(y_values_temp))
        y_values = np.array(y_values_temp)

        data = np.column_stack((x_indices, y_values))
        # print(data)
        return data