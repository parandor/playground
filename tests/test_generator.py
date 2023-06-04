import numpy as np

from data.generator import DataGenerator
from detection.detector import TroughDetector

data_generator = DataGenerator(
    num_points=100, start_value=40, middle_value=25, end_value=20,
    noise_factor=0.2)
data = data_generator.generate_data()
x_values, y_values = data
# data_generator.plot_data(x_values, y_values)

# Print the generated x and y values to the console
for i in range(data_generator.num_points):
    print(f'{x_values[i]:.1f}s\t{y_values[i]:.3f}')

# Create TroughDetector instance
data = np.column_stack((x_values, y_values))
trough_detector = TroughDetector(data)

# Detect troughs
trough_indices = trough_detector.detect_troughs()
print("Detected Trough Indices:", trough_indices)

# Plot data with detected troughs
trough_detector.plot_troughs()


# # Example data
# x_values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# y_values = np.array([2.5, 2.1, 1.8, 2.4, 2.7, 1.9, 1.5, 2.0, 1.7, 2.3])
# data = np.column_stack((x_values, y_values))

# # Create TroughDetector instance
# trough_detector = TroughDetector(data)

# # Detect troughs
# trough_indices = trough_detector.detect_troughs()
# print("Detected Trough Indices:", trough_indices)

# # Plot data with detected troughs
# trough_detector.plot_troughs()
