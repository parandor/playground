import RPi.GPIO as GPIO
import time
from sensors.sensor_base import SensorBase


class UltrasonicSensor(SensorBase):
    def __init__(self, trigger_pin, echo_pin, buf_size, sensor_id):
        super().__init__(buffer_size=buf_size, sensor_id=sensor_id)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.num_readings = 5

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
            self.update_average(sum(distances) / len(distances))

    def cleanup(self):
        GPIO.cleanup()