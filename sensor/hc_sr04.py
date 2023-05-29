import RPi.GPIO as GPIO
import time
from collections import deque
import numpy as np

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin, buf_size, sensor_id):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.buffer_size = buf_size
        self.num_readings = 5
        self.distance_buffer = deque(maxlen=self.buffer_size)
        self.sensor_id = sensor_id
        self.average = 0.0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def is_connected(self):
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        GPIO.output(self.trigger_pin, GPIO.LOW)

        if GPIO.input(self.echo_pin):
            return True
        return False

    def _get_distance(self):
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
                distance = self._get_distance()
                distances.append(distance)
                time.sleep(0.2)  # Delay between readings to avoid interference
            except Exception as e:
                print("Error:", str(e))

        if len(distances) > 0:
            self.average = sum(distances) / len(distances)
            self.distance_buffer.append(self.average)

    def get_distance_buffer(self):
        distance_array = np.array(self.distance_buffer)
        x_indices = np.arange(len(distance_array))
        return np.column_stack((x_indices, distance_array))
    
    def get_average_distance(self):
        return self.average

    def cleanup(self):
        GPIO.cleanup()
