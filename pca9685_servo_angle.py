# in Thonny   >>> %Run pca9685_servo_angle.py 1 100	
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16, address=0x40) #0x6F,0x41
import sys
kit.servo[int(sys.argv[1])].angle = int(sys.argv[2])
