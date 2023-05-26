import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

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

    def average_distance(self, num_readings):
        distances = []

        for _ in range(num_readings):
            try:
                distance = self.get_distance()
                distances.append(distance)
                time.sleep(0.1)  # Delay between readings to avoid interference
            except Exception as e:
                print("Error:", str(e))

        if len(distances) > 0:
            average = sum(distances) / len(distances)
            return average
        else:
            return None

    def cleanup(self):
        GPIO.cleanup()

# Example usage
try:
    trigger_pin = 22
    echo_pin = 19

    sensor = UltrasonicSensor(trigger_pin, echo_pin)
    num_readings = 5
    while True:
        try:
            average_dist = sensor.average_distance(num_readings)        
            if average_dist is not None:
                print(f"Distance: {average_dist:.1f} cm")
            else:
                print("No readings available.")
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("Measurement interrupted.")
            break
    
except Exception as e:
    print("Error:", str(e))

finally:
    if 'sensor' in locals():
        sensor.cleanup()
