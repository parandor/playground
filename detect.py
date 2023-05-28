from detection.detector import TroughDetector
from file.writer import IOHandler
from sensor.distance import UltrasonicSensor
from sound.beep import SoundPlayer
from storage.database.influx import InfluxDBSender
import time
import uuid


# Example usage
try:
    trigger_pin = 22
    echo_pin = 19
    buf_size = 2000
    filename = "sensor_data.csv"
    sensor_id = "HC-SR04_EM78P153A_" + str(uuid.uuid4())

    sensor = UltrasonicSensor(trigger_pin, echo_pin, buf_size, sensor_id)
    beeper = SoundPlayer()
    
    # Configure your InfluxDB connection parameters
    host = '192.168.1.233'
    port = '8086'
    username = 'admin'
    password = 'admin'
    database = 'influx'

    # Create an instance of the InfluxDBSender class
    sender = InfluxDBSender(host, port, username, password, database)

    # Connect to the InfluxDB server
    sender.connect()
    
    while True:
        try:
            sensor.average_distance()    
            buf = sensor.get_distance_buffer()
            avg = sensor.get_average_distance()    
            IOHandler.write_numpy("buffer.csv", buf)

            data_measurement = "sensors"
            data_tags = {
                "sensor_id": sensor_id,
                "type": "distance",
                "location": "Peter's office"
            }
            data_fields = {
                "value": avg
            }
            # Send the data to the InfluxDB server
            sender.send_data(data_measurement, data_tags, data_fields)

            # y_values = buf[:, 1]  # Extract the second column (y values)
            # formatted_values = ["{:.3f}".format(value) for value in y_values]
            # print(" ".join(formatted_values))
                
            detector = TroughDetector(buf)
            detector.detect_troughs()

            discretized_data = detector.discretize_data(buf)
            smoothed_data = detector.get_smoothed_data(discretized_data)
            IOHandler.write_numpy("smoothed.csv", smoothed_data.astype(int))

            filtered_data = detector.get_filtered_data()
            IOHandler.write_numpy("filtered.csv", filtered_data.astype(int))
            
            # formatted_values = ["{:.0f}".format(value) for value in filtered_data]
            # print(" ".join(formatted_values))

            if detector.is_trough_detected():
                print("Detected Trough Indices:", detector.get_troughs())
                beeper.beep()
            else:
                beeper.beep_off()

            time.sleep(1)
                    
        except KeyboardInterrupt:
            print("Measurement interrupted.")
            break
    
except Exception as e:
    print("Error:", str(e))

finally:
    if 'sensor' in locals():
        sensor.cleanup()
