import RPi.GPIO as GPIO
import time
from collections import deque
import numpy as np

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, buf_size):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.buffer_size = buf_size
        self.num_readings = 3
        self.distance_buffer = deque(maxlen=self.buffer_size)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        pulse_start = time.time()
        pulse_end = time.time()

        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300 / 2  # Speed of sound is 343 meters/second
        return distance

    def average_distance(self):
        distances = []

        for _ in range(self.num_readings):
            try:
                distance = self.get_distance()
                distances.append(distance)
                time.sleep(0.02)  # Delay between readings to avoid interference
            except Exception as e:
                print("Error:", str(e))

        if len(distances) > 0:
            average = sum(distances) / len(distances)
            self.distance_buffer.append(average)

    def get_distance_buffer(self):
        distance_array = np.array(self.distance_buffer)
        x_indices = np.arange(len(distance_array))
        return np.column_stack((x_indices, distance_array))

    def cleanup(self):
        GPIO.cleanup()
