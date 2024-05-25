#include <Servo.h> 
const int servoCenter = 90;
const int servoRange = 20;
const int lidOpen = 130;
const int lidClose = 90;
const int leftLid = 3;
const int leftPan = 5;
const int leftTilt = 6;
const int rightLid = 9;
const int rightPan = 10;
const int rightTilt = 11;

Servo panServoL, tiltServoL, lidServoL;
Servo panServoR, tiltServoR, lidServoR;

int pan_servopos, tilt_servopos;
int pan_servopos_L, tilt_servopos_L;
int pan_servopos_R, tilt_servopos_R;
int dataIn[4] = {255, 0, 100, 100}; // Array to store information (255, button, X, Y)
int in_byte = 0; // Variable to store incoming byte
int array_index = 0; // Index for the dataIn array

void setup(){
  Serial.begin(38400);
  lidServoL.attach(leftLid);//assigning servo pin
  panServoL.attach(leftPan);
  tiltServoL.attach(leftTilt);
  lidServoR.attach(rightLid);
  panServoR.attach(rightPan);
  tiltServoR.attach(rightTilt);

  lidServoL.write(lidOpen);//initial servo angle
  panServoL.write(servoCenter);
  tiltServoL.write(servoCenter);
  lidServoR.write(lidOpen);
  panServoR.write(servoCenter);
  tiltServoR.write(servoCenter);

}

void loop(){
  if(Serial.available()> 0 ){ 
    in_byte = Serial.read(); // Read the incoming byte
    if (in_byte == 255) { // Check if the byte is the start indicator
      array_index = 0; // Reset array index
    }
    dataIn[array_index] = in_byte; // Store in the dataIn array
    array_index = array_index + 1; // Increment the array index
  }
    pan_servopos = map(dataIn[2]-100, -100, 100, -servoRange, servoRange); //incoming x or y (0 ~ 200) to (-100 ~ +100)
    tilt_servopos = map(dataIn[3]-100, -100, 100, -servoRange, servoRange);//then map to between (-20 ~ +20 degree)
    if (dataIn[1] == 1){//both eyes move normally
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      panServoL.write(servoCenter+pan_servopos); //move servo either +20 or -20 from center position
      tiltServoL.write(servoCenter+tilt_servopos);
      panServoR.write(servoCenter+pan_servopos);
      tiltServoR.write(servoCenter+tilt_servopos);
    }
    else if (dataIn[1] == 2){//both eyes move symetrically in the y-axis
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      panServoL.write(servoCenter+pan_servopos);
      tiltServoL.write(servoCenter+tilt_servopos);
      panServoR.write(servoCenter-pan_servopos);
      tiltServoR.write(servoCenter+tilt_servopos);
    }
    else if (dataIn[1] == 3){//both eyes move symetrically in the x and y axises
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      panServoL.write(servoCenter+pan_servopos);
      tiltServoL.write(servoCenter+tilt_servopos);
      panServoR.write(servoCenter-pan_servopos);
      tiltServoR.write(servoCenter-tilt_servopos);
    }    
    else if (dataIn[1] == 4){// only left eye moves
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      panServoL.write(servoCenter+pan_servopos);
      tiltServoL.write(servoCenter+tilt_servopos);
    }
    else if (dataIn[1] == 6){//only right eye moves
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      panServoR.write(servoCenter+pan_servopos);
      tiltServoR.write(servoCenter+tilt_servopos);
    }                
    else if (dataIn[1] == 7){//both eyes blink
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      lidServoL.write(lidClose);
      lidServoR.write(lidClose);
      delay(50);
      lidServoL.write(lidOpen);
      lidServoR.write(lidOpen);
    }    
    else if (dataIn[1] == 8){//right eye blinks
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      lidServoR.write(lidClose);
      delay(50);
      lidServoR.write(lidOpen);
    }        
    else if (dataIn[1] == 9){//left eye blinks
      Serial.println((String)"button= "+dataIn[1]+(String)"; x= "+pan_servopos+(String)"; y= "+tilt_servopos); 
      lidServoL.write(lidClose);
      delay(50);
      lidServoL.write(lidOpen);
    }    
}
