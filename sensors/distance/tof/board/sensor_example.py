from sensors.distance.tof.board.sensor import DistanceSensor
import time


# Example usage
buffer_size = 200
sensor_id = "VL53L1X_MODELID_0xEA"
sensor = DistanceSensor(buffer_size, sensor_id)
sensor.print_info()
sensor.start_ranging()

try:
    while True:
        distance = sensor.get_distance()
        if distance is not None:
            print("Distance: {} cm".format(distance))
        time.sleep(0.2)
except KeyboardInterrupt:
    sensor.cleanup()