import cv2
import mediapipe as mp
import time
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16,address=0x40) # Initialize servo controller
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
cols, rows =640, 480

pTime = 0.0 #time tracking for FPS
cTime = 0.0


with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
    while True:
        image= picam2.capture_array()
        image=cv2.flip(image, 0)

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                location_data = detection.location_data
                if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
                    bb = location_data.relative_bounding_box
                bb_box = [
                bb.xmin, bb.ymin,
                bb.width, bb.height,
              ]
                relative_x = int(bb.xmin * cols)
                relative_y = int(bb.ymin * rows)
                relative_x_w = int((bb.xmin+bb.width) * cols)
                relative_y_h = int((bb.ymin+bb.height) * rows)
                face_center_x=(relative_x+relative_x_w)//2
                face_center_y=(relative_y+relative_y_h)//2
                move_x=int(((face_center_x-320) - (-320)) * (eye_max - (eye_min)) / (320 - (-320)) + (eye_min));            
                move_y=int(((face_center_y-240) - (-240)) * (eye_max - (eye_min)) / (240 - (-240)) + (eye_min));
#                 print(eye_center+move_x, eye_center+move_y)
                kit.servo[PAN_CHANNEL_L].angle = eye_center-move_x
                kit.servo[TILT_CHANNEL_L].angle = eye_center+move_y
                kit.servo[PAN_CHANNEL_R].angle = eye_center-move_x
                kit.servo[TILT_CHANNEL_R].angle = eye_center+move_y

                cv2.rectangle(image, (relative_x, relative_y), (relative_x_w, relative_y_h),
                         (0, 255, 255), 1)  # draw bounding box of face (yellow)
                cv2.line(image, (face_center_x, 0), (face_center_x, rows), (0, 255, 255), 1)
                cv2.line(image, (0, face_center_y), (cols,face_center_y), (0, 255, 255), 1) 
        cTime = time.time() # calculate and display FPS
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(image, f"FPS : {int(fps)}", (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) 
        cv2.imshow("Frame", image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
kit.servo[PAN_CHANNEL_L].angle = pan_initial_angle 
kit.servo[TILT_CHANNEL_L].angle = tilt_initial_angle
kit.servo[LID_CHANNEL_L].angle = lid_initial_angle
kit.servo[PAN_CHANNEL_R].angle = pan_initial_angle 
kit.servo[TILT_CHANNEL_R].angle = tilt_initial_angle
kit.servo[LID_CHANNEL_R].angle = lid_initial_angle
time.sleep(1)

cv2.destroyAllWindows()
