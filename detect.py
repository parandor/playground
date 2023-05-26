from sensor.distance import UltrasonicSensor
from detection.detector import TroughDetector
import time

# Example usage
try:
    trigger_pin = 22
    echo_pin = 19

    sensor = UltrasonicSensor(trigger_pin, echo_pin)
    num_readings = 5
    while True:
        try:
            sensor.average_distance(num_readings)    
            buf = sensor.get_distance_buffer()    
            y_values = buf[:, 1]  # Extract the second column (y values)
            formatted_values = ["{:.3f}".format(value) for value in y_values]
            print(" ".join(formatted_values))
            # if buf is not None:
            #     print("Distance buf: %s", buf)
            # else:
            #     print("No readings available.")
                
            # Create TroughDetector instance
            trough_detector = TroughDetector(buf, discretization_factor=10000)


            smoothed_data = trough_detector.get_smoothed_data()
            formatted_values = ["{:.0f}".format(value) for value in smoothed_data]
            print(" ".join(formatted_values))

            # Detect troughs
            trough_indices = trough_detector.detect_troughs()
            print("Detected Trough Indices:", trough_indices)

            time.sleep(0.2)
                    
        except KeyboardInterrupt:
            print("Measurement interrupted.")
            break
    
except Exception as e:
    print("Error:", str(e))

finally:
    if 'sensor' in locals():
        sensor.cleanup()
