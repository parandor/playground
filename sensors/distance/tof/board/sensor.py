import board
import adafruit_vl53l1x
from sensors.sensor_base import SensorBase


class DistanceSensor(SensorBase):
    def __init__(self, buffer_size):
        super().__init__(buffer_size=buffer_size)
        self.i2c = board.I2C()
        self.vl53 = adafruit_vl53l1x.VL53L1X(self.i2c)
        self.vl53.distance_mode = 1
        self.vl53.timing_budget = 100

    def print_info(self):
        print("VL53L1X Simple Test.")
        print("--------------------")
        model_id, module_type, mask_rev = self.vl53.model_info
        print("Model ID: 0x{:0X}".format(model_id))
        print("Module Type: 0x{:0X}".format(module_type))
        print("Mask Revision: 0x{:0X}".format(mask_rev))
        print("Distance Mode: ", end="")
        if self.vl53.distance_mode == 1:
            print("SHORT")
        elif self.vl53.distance_mode == 2:
            print("LONG")
        else:
            print("UNKNOWN")
        print("Timing Budget: {}".format(self.vl53.timing_budget))
        print("--------------------")

    def start_ranging(self):
        self.vl53.start_ranging()

    def get_distance(self):
        if self.vl53.data_ready:
            distance = self.vl53.distance
            self.vl53.clear_interrupt()
            self.update_average(distance)
            return distance
        else:
            return None

    def cleanup(self):
        self.vl53.stop_ranging()
        self.i2c.deinit()

# # Example usage
# sensor = DistanceSensor()
# sensor.print_info()
# sensor.start_ranging()

# try:
#     while True:
#         distance = sensor.get_distance()
#         if distance is not None:
#             print("Distance: {} cm".format(distance))
#         time.sleep(0.2)
# except KeyboardInterrupt:
#     sensor.cleanup()
