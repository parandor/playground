import time

from detection.detector import TroughDetector
from sensors.distance.ultrasonic.gpio.sensor import UltrasonicSensor
from sensors.distance.tof.board.sensor import DistanceSensor
from sound.beep import SoundPlayer
from storage.database.influx import InfluxDBSender


try:
    # trigger_pin = 22
    # echo_pin = 19
    # sensor_id = "HC-SR04_EM78P153A"
    # sensor = UltrasonicSensor(trigger_pin, echo_pin, buf_size, sensor_id)   
    
    sensor_id = "VL53L1X_MODELID_0xEA"
    buf_size = 2000
    sensor = DistanceSensor(buf_size, sensor_id)
    sensor.print_info()
    sensor.start_ranging()

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
            sensor.get_distance()    
            buf = sensor.get_distance_buffer()

            if buf is not None and len(buf) > 0:
                data_measurement = "sensors"
                data_location = "Peter's office"
                data_tags = {
                    "location": data_location,
                    "sensor_id": sensor_id,
                    "type": "distance_raw"
                }
                for timestamp, value in zip(sensor.get_timestamps(), buf[:, 1]):
                    sender.send_data(data_measurement, data_tags, value, timestamp)
                    
                detector = TroughDetector(buf)
                detector.detect_troughs()

                smoothed_data = detector.filter.smoothed_data
                if smoothed_data is not None and len(smoothed_data) > 0:
                    data_tags = {
                        "location": data_location,
                        "sensor_id": sensor_id,
                        "type": "distance_smoothed"
                    }
                    for timestamp, value in zip(sensor.get_timestamps(), smoothed_data):
                        sender.send_data(data_measurement, data_tags, value, timestamp)

                filtered_data = detector.filter.filtered_data
                if filtered_data is not None and len(filtered_data) > 0:
                    data_tags = {
                        "location": data_location,
                        "sensor_id": sensor_id,
                        "type": "distance_filtered"
                    }
                    for timestamp, value in zip(sensor.get_timestamps(), filtered_data):
                        sender.send_data(data_measurement, data_tags, value, timestamp)
    
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
