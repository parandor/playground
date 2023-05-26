import RPi.GPIO as GPIO
import time


class UltrasonicSensor:
    def __init__(self, trig_pin=22, echo_pin=19):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, GPIO.LOW)

        pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        speed_of_sound = 34300  # Speed of sound in cm/s
        distance = (pulse_duration * speed_of_sound) / 2

        return distance

    def cleanup(self):
        GPIO.cleanup()


if __name__ == '__main__':
    try:
        sensor = UltrasonicSensor()
        sensor.setup()
        while True:
            distance = sensor.get_distance()
            print(f"Distance: {distance:.1f} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("User interrupt triggered")
    finally:
        sensor.cleanup()
