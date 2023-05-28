from datetime import datetime
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError


class InfluxDBSender:
    def __init__(self, host, port, username, password, database):
        self.client = InfluxDBClient(host=host, port=port, username=username,
                                     password=password)
        self.database = database

    def connect(self):
        try:
            self.client.switch_database(self.database)
            print("Connected to InfluxDB database:", self.database)
        except Exception as e:
            print("Failed to connect to InfluxDB:", str(e))
            
    def send_data(self, measurement, tags, fields):
        # Convert the timestamp to the InfluxDB format
        t_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = [
            {
                "measurement": measurement,
                "time": t_now,
                "tags": tags,
                "fields": fields
            }
        ]
        try:
            self.client.write_points(data)
        except InfluxDBClientError as e:
            print("Failed to send data to InfluxDB:", str(e))
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            
    def close(self):
        self.client.close()
        print("Connection to InfluxDB closed")


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

    # Close the connection
    sender.close()
