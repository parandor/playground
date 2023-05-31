from datetime import datetime
from collections import deque
import numpy as np

class SensorBase:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.distance_buffer = deque(maxlen=self.buffer_size)
        self.timestamps = deque(maxlen=self.buffer_size)
        self.average = 0.0

    def update_average(self, distance):
        self.distance_buffer.append(distance)
        self.timestamps.append(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.average = sum(self.distance_buffer) / len(self.distance_buffer)

    def get_distance_buffer(self):
        distance_array = np.array(self.distance_buffer)
        x_indices = np.arange(len(distance_array))
        return np.column_stack((x_indices, distance_array))

    def get_timestamps(self):
        return self.timestamps

    def get_average_distance(self):
        return self.average
