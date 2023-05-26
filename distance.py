import RPi.GPIO as GPIO
import time

# GPIO pin numbers
TRIG_PIN = 22
ECHO_PIN = 19

def setup():
    GPIO.setmode(GPIO.BCM)

    # Setup GPIO pins
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Send a short pulse to trigger the ultrasonic sensor
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Wait for the echo response
    pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the pulse duration and convert it to distance
    pulse_duration = pulse_end - pulse_start
    speed_of_sound = 34300  # Speed of sound in cm/s
    distance = (pulse_duration * speed_of_sound) / 2

    return distance

def cleanup():
    GPIO.cleanup()

# Main program
if __name__ == '__main__':
    try:
        setup()
        while True:
            distance = get_distance()
            print(f"Distance: {distance:.1f} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("User interrupt triggered")
        pass
    finally:
        cleanup()
