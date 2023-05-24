from influxdb import InfluxDBClient

class InfluxDBSender:
    def __init__(self, host, port, username, password, database):
        self.client = InfluxDBClient(host=host, port=port, username=username, password=password)
        self.database = database
    
    def connect(self):
        try:
            self.client.switch_database(self.database)
            print("Connected to InfluxDB database:", self.database)
        except Exception as e:
            print("Failed to connect to InfluxDB:", str(e))
    
    def send_data(self, data):
        try:
            self.client.write_points(data)
            print("Data sent successfully")
        except Exception as e:
            print("Failed to send data to InfluxDB:", str(e))
    
    def close(self):
        self.client.close()
        print("Connection to InfluxDB closed")


# Example usage:
if __name__ == '__main__':
    # Configure your InfluxDB connection parameters
    host = 'localhost'
    port = '8086'
    username = 'admin'
    password = 'admin'
    database = 'influx'
    
    # Create an instance of the InfluxDBSender class
    sender = InfluxDBSender(host, port, username, password, database)
    
    # Connect to the InfluxDB server
    sender.connect()
    
    # Define the data points you want to send
    data = [
        {
            "measurement": "temperature",
            "tags": {
                "location": "room1"
            },
            "fields": {
                "value": 25.0
            }
        }
    ]
    
    # Send the data to the InfluxDB server
    sender.send_data(data)
    
    # Close the connection
    sender.close()
