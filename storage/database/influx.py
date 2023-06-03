from datetime import datetime, timedelta
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
            
    def send_data(self, measurement, tags, field, timestamp):
        data_point = {
            "measurement": measurement,
            "time": timestamp,
            "tags": tags,
            "fields": {"value": field}
        }

        try:
            self.client.write_points([data_point])
        except InfluxDBClientError as e:
            print("Failed to send data to InfluxDB:", str(e))
        except Exception as e:
            print("An unexpected error occurred:", str(e))

    def query_last_2_days(self):
        end_time = datetime.utcnow()  # Current UTC time
        start_time = end_time - timedelta(days=2)

        query = f'SELECT * FROM /.*/ WHERE time >= \'{start_time.strftime("%Y-%m-%dT%H:%M:%SZ")}\' AND time <= \'{end_time.strftime("%Y-%m-%dT%H:%M:%SZ")}\''
        result = self.client.query(query)
        return result.get_points()

    def get_mean_value_in_time_range(self, measurement, field, tag_conditions, time_range, group_interval):
        # Build the InfluxDB query
        conditions = [f'("{tag}"::tag = \'{value}\')' for tag, value in tag_conditions.items()]
        query = f'SELECT mean("{field}") FROM "{measurement}" WHERE {" AND ".join(conditions)}'
        query += f' AND time >= now() - {time_range} and time <= now() GROUP BY time({group_interval}) fill(null)'
            
        result = self.client.query(query)
        return result.get_points()

    def close(self):
        self.client.close()
        print("Connection to InfluxDB closed")

