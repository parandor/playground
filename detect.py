from sensor.distance import UltrasonicSensor
from detection.detector import TroughDetector
from sound.beep import SoundPlayer
import time

# Example usage
try:
    trigger_pin = 22
    echo_pin = 19

    sensor = UltrasonicSensor(trigger_pin, echo_pin)
    beeper = SoundPlayer()
    while True:
        try:
            sensor.average_distance()    
            buf = sensor.get_distance_buffer()    
            # y_values = buf[:, 1]  # Extract the second column (y values)
            # formatted_values = ["{:.3f}".format(value) for value in y_values]
            # print(" ".join(formatted_values))
                
            detector = TroughDetector(buf)

            # Detect troughs
            detector.detect_troughs()

            filtered_data = detector.get_filtered_data()
            formatted_values = ["{:.0f}".format(value) for value in filtered_data]
            print(" ".join(formatted_values))

            if detector.is_trough_detected():
                print("Detected Trough Indices:", detector.get_troughs())
                beeper.beep()
            else:
                beeper.beep_off()

            time.sleep(0.05)
                    
        except KeyboardInterrupt:
            print("Measurement interrupted.")
            break
    
except Exception as e:
    print("Error:", str(e))

finally:
    if 'sensor' in locals():
        sensor.cleanup()
