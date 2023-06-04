from storage.database.influx import InfluxDBSender
from detection.detector import TroughDetector
from detection.roc_detector import RateOfChangeDetector
from data.convert import Converter

def send_sample_data(sender):
    # Send the data associated with the sensor
    data_measurement = "sensors"
    data_tags = {
        "sensor_id": "HC-SR04_asdlkjasld_aksjdak",
        "type": "distance",
        "location": "Peter's office"
    }
    data_fields = {
        "field1": 1,
        "field2": 2
    }
    
    # Send the data to the InfluxDB server
    sender.send_data(data_measurement, data_tags, data_fields)


# Example usage:
if __name__ == '__main__':
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

    # Get sensor data from the database
    tag_conditions = {
        'type': 'distance_raw',
        'sensor_id': 'VL53L1X_MODELID_0xEA'
    }
    data = sender.get_mean_value_in_time_range("sensors", "value", tag_conditions, '2d', '1m')
    
    data_stacked = Converter.to_col_stack_with_mean(data)
    
    detector = TroughDetector(data_stacked)
    detector.detect_troughs()
    detector.plot_troughs_filtered()

    # roc = RateOfChangeDetector(data_stacked)
    # indices = roc.detect_decline()
        
    # Send the data associated with the sensor
    # send_sample_data(sender)

    # Close the connection
    sender.close()
    
