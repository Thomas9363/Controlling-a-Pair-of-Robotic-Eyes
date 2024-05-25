import bluetooth
from adafruit_servokit import ServoKit
import time
# servo channels initization
kit = ServoKit(channels=16,address=0x40 )
LID_CHANNEL_L, PAN_CHANNEL_L,TILT_CHANNEL_L = 0, 1, 2
LID_CHANNEL_R, PAN_CHANNEL_R,TILT_CHANNEL_R = 4, 5, 6

lid_initial_angle=140
pan_initial_angle=90
tilt_initial_angle=90
eye_min, eye_max =-20, 20
lid_min, lid_max=90, 140
eye_center=90
kit.servo[PAN_CHANNEL_L].angle = pan_initial_angle
kit.servo[TILT_CHANNEL_L].angle = tilt_initial_angle
kit.servo[LID_CHANNEL_L].angle = lid_initial_angle
kit.servo[PAN_CHANNEL_R].angle = pan_initial_angle
kit.servo[TILT_CHANNEL_R].angle = tilt_initial_angle
kit.servo[LID_CHANNEL_R].angle = lid_initial_angle
# Create a Bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# Set the port number for the server socket
port = 27
server_sock.bind(("", port))
# Listen for incoming connections from clients
server_sock.listen(1)
# Accept the client connection
client_sock, address = server_sock.accept()
print("connection made with:", address)
# Initialize a list to store data received in 255-based groups
dataIn = [255, 0, 100, 100]
# Initialize an index to keep track of dataIn elements
array_index = 0
while True:
    try:
        # Receive data from the client
        data = client_sock.recv(1024)
        # Convert the received data (bytes) to an integer
        in_byte = int.from_bytes(data, byteorder='big')
        # If the received byte is 255, it indicates the start of a new group
        if in_byte == 255:
            array_index = 0
        # Add the received integer to the dataIn list at the current index
        dataIn[array_index] = in_byte
        array_index += 1
        # When array_index reaches 4, a complete group is received, so print the values
        if array_index == 4:
            if dataIn[2] >=200:
                dataIn[2]=200
            if dataIn[3]>=200:
                dataIn[3]=200
            dataIn[2]=int(((dataIn[2]-100) - (-100)) * (eye_max - (eye_min)) / (100 - (-100)) + (eye_min));            
            dataIn[3]=int(((dataIn[3]-100) - (-100)) * (eye_max - (eye_min)) / (100 - (-100)) + (eye_min));
            pan_angle=eye_center+dataIn[2]
            tilt_angle=eye_center+dataIn[3]
            if dataIn[1] == 1:
                kit.servo[PAN_CHANNEL_L].angle = eye_center+dataIn[2]
                kit.servo[TILT_CHANNEL_L].angle = eye_center+dataIn[3]
                kit.servo[PAN_CHANNEL_R].angle = eye_center+dataIn[2]
                kit.servo[TILT_CHANNEL_R].angle = eye_center+dataIn[3]
            elif dataIn[1] == 2:
                kit.servo[PAN_CHANNEL_L].angle = eye_center+dataIn[2]
                kit.servo[TILT_CHANNEL_L].angle = eye_center+dataIn[3]
                kit.servo[PAN_CHANNEL_R].angle = eye_center-dataIn[2]
                kit.servo[TILT_CHANNEL_R].angle = eye_center+dataIn[3]
            elif dataIn[1] == 3:
                kit.servo[PAN_CHANNEL_L].angle = eye_center+dataIn[2]
                kit.servo[TILT_CHANNEL_L].angle = eye_center+dataIn[3]
                kit.servo[PAN_CHANNEL_R].angle = eye_center-dataIn[2]
                kit.servo[TILT_CHANNEL_R].angle = eye_center-dataIn[3]               
            elif dataIn[1] == 4:
                kit.servo[PAN_CHANNEL_L].angle = eye_center+dataIn[2]
                kit.servo[TILT_CHANNEL_L].angle = eye_center+dataIn[3]
            elif dataIn[1] == 6:
                kit.servo[PAN_CHANNEL_R].angle = eye_center+dataIn[2]
                kit.servo[TILT_CHANNEL_R].angle = eye_center+dataIn[3]                              
            elif dataIn[1] == 7:
                kit.servo[LID_CHANNEL_L].angle = lid_min
                kit.servo[LID_CHANNEL_R].angle = lid_min
                time.sleep(0.2)
                kit.servo[LID_CHANNEL_L].angle = lid_max
                kit.servo[LID_CHANNEL_R].angle = lid_max
            elif dataIn[1] == 8:
                kit.servo[LID_CHANNEL_L].angle = lid_min
                time.sleep(0.2)
                kit.servo[LID_CHANNEL_L].angle = lid_max   
            elif dataIn[1] == 9:
                kit.servo[LID_CHANNEL_R].angle = lid_min
                time.sleep(0.2)
                kit.servo[LID_CHANNEL_R].angle = lid_max               
#             print("divide:", dataIn[0], " button:", dataIn[1]," X:",dataIn[2],"Y:", dataIn[3])
            print("divide:", dataIn[0], " button:", dataIn[1]," X:",pan_angle,"Y:", tilt_angle)
            print()
        # Ensure array_index stays within the range of dataIn (0 to 3)
        array_index %= len(dataIn)
    except IOError:
        break
kit.servo[PAN_CHANNEL_L].angle = pan_initial_angle 
kit.servo[TILT_CHANNEL_L].angle = tilt_initial_angle
kit.servo[LID_CHANNEL_L].angle = lid_initial_angle
kit.servo[PAN_CHANNEL_R].angle = pan_initial_angle 
kit.servo[TILT_CHANNEL_R].angle = tilt_initial_angle
kit.servo[LID_CHANNEL_R].angle = lid_initial_angle
time.sleep(1)
# Close the client and server sockets
client_sock.close()
server_sock.close()
