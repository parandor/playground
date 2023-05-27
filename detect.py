from detection.detector import TroughDetector
from file.writer import IOHandler
from sensor.distance import UltrasonicSensor
from sound.beep import SoundPlayer
import time


# Example usage
try:
    trigger_pin = 22
    echo_pin = 19
    buf_size = 2000
    filename = "sensor_data.csv"

    sensor = UltrasonicSensor(trigger_pin, echo_pin, buf_size)
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
            IOHandler.write_numpy(filename, filtered_data.astype(int))
            # ddata = detector.discretize_data()
            # IOHandler.write_numpy(filename, ddata)
            
            # formatted_values = ["{:.0f}".format(value) for value in filtered_data]
            # print(" ".join(formatted_values))

            if detector.is_trough_detected():
                print("Detected Trough Indices:", detector.get_troughs())
                beeper.beep()
            else:
                beeper.beep_off()

            time.sleep(15)
                    
        except KeyboardInterrupt:
            print("Measurement interrupted.")
            break
    
except Exception as e:
    print("Error:", str(e))

finally:
    if 'sensor' in locals():
        sensor.cleanup()
