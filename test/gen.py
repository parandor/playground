import numpy as np
import matplotlib.pyplot as plt


class TestDataGenerator:
    """
    Class for generating sample test data in the shape of a sideways S curve with added noise.
    """

    def __init__(self, num_points=100, start_value=40, middle_value=25, end_value=20, noise_factor=0.3):
        """
        Initialize the TestDataGenerator.

        Args:
            num_points (int): Number of data points to generate.
            start_value (float): Start value of the y-axis.
            middle_value (float): Middle value of the y-axis.
            end_value (float): End value of the y-axis.
            noise_factor (float): Scaling factor for the noise.
        """
        self.num_points = num_points
        self.start_value = start_value
        self.middle_value = middle_value
        self.end_value = end_value
        self.noise_factor = noise_factor

    def generate_data(self):
        """
        Generate the test data.

        Returns:
            tuple: Tuple containing the x-axis values and y-axis values.
        """
        x = np.linspace(0, 100, self.num_points)  # Time scale in seconds
        y = -((self.start_value - self.middle_value) *
              np.sin(x / 50 * np.pi)) + self.start_value
        influence_factor = np.exp(-0.03 * x)  # Exponential decay factor
        y = (self.start_value - y) * influence_factor + y
        # Flattens out to the end value
        y += (self.end_value - y[-1]) * (1 - influence_factor)

        noise = np.random.uniform(-self.noise_factor,
                                  self.noise_factor, self.num_points)
        y += noise * 0.5  # Scale the noise by a factor of 0.5

        return x, y


# Example usage
data_generator = TestDataGenerator(
    num_points=100, start_value=40, middle_value=25, end_value=20, noise_factor=0.2)
x_values, y_values = data_generator.generate_data()

# Print the generated x and y values to the console
for i in range(data_generator.num_points):
    print(f'{x_values[i]:.1f}s\t{y_values[i]:.3f}')

# Plot the generated test data
plt.plot(x_values, y_values)
plt.xlabel('Time (seconds)')
plt.ylabel('Y')
plt.title('Sample Test Data')
plt.grid(True)
plt.show()
