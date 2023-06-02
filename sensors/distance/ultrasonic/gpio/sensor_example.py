from sensors.distance.ultrasonic.gpio.sensor import UltrasonicSensor


#Example usage

trigger_pin = 22
echo_pin = 19
sensor_id = "HC-SR04_EM78P153A"
buf_size = 200
sensor = UltrasonicSensor(trigger_pin, echo_pin, buf_size, sensor_id)   

sensor.average_distance()    
buf = sensor.get_distance_buffer()