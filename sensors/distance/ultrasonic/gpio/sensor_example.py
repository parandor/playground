from sensors.distance.ultrasonic.gpio.sensor import UltrasonicSensor
import time


#Example usage
trigger_pin = 22
echo_pin = 19
sensor_id = "HC-SR04_EM78P153A"
buf_size = 200
sensor = UltrasonicSensor(trigger_pin, echo_pin, buf_size, sensor_id)   

try:
    while True:
        sensor.average_distance()    
        distance = sensor.get_average_distance()        
        if distance is not None:
            print("Distance: {} cm".format(distance))
        time.sleep(0.2)
except KeyboardInterrupt:
    sensor.cleanup()
