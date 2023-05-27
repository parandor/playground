from sensor.distance import UltrasonicSensor
from detection.detector import TroughDetector
from sound.beep import SoundPlayer
import time

# Example usage
try:
    trigger_pin = 22
    echo_pin = 19

    sensor = UltrasonicSensor(trigger_pin, echo_pin)
    # Create an instance of BeepSound
    player = SoundPlayer()
    while True:
        try:
            sensor.average_distance()    
            buf = sensor.get_distance_buffer()    
            y_values = buf[:, 1]  # Extract the second column (y values)
            # formatted_values = ["{:.3f}".format(value) for value in y_values]
            # print(" ".join(formatted_values))
                
            # Create TroughDetector instance
            trough_detector = TroughDetector(buf)

            smoothed_data = trough_detector.get_smoothed_data(trough_detector.discretize_data())
            formatted_values = ["{:.0f}".format(value) for value in smoothed_data]
            print(" ".join(formatted_values))

            # Detect troughs
            trough_detector.detect_troughs()
            if trough_detector.is_trough_detected():
                print("Detected Trough Indices:", trough_detector.get_troughs())
                player.beep()
            else:
                player.beep_off()

            time.sleep(0.05)
                    
        except KeyboardInterrupt:
            print("Measurement interrupted.")
            break
    
except Exception as e:
    print("Error:", str(e))

finally:
    if 'sensor' in locals():
        sensor.cleanup()
