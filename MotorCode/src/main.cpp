#include <Arduino.h>
#include <Servo.h>


/** Controls
 * 
 * Movement commands:
 *  forward, backward, stop
 *  slow, medium
 * 
 * Rotation commands:
 *  left, right
 * 
 * After starting, the motors will continue moving until `stop` is sent.
 * This allows the wheels to continue moving forward while rotation commands are sent.
 * While rotation commands are not being sent, the wheels will align themselves straight again.
 */

int motor1pin1 = 2;
int motor1pin2 = 3;

int motorSpeedPin = 9;

int servo1pin = 4;
int servo2pin = 5;

Servo servo1;
Servo servo2;

int angle = 0;
int speed = 255;

const int MAX_ROTATION = 40;
const int ROTATION_SPEED = 5;
const int ROTATION_BRAKING = 2;


void setup() {
  Serial.begin(115200); // baudrate

  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);

  pinMode(motorSpeedPin, OUTPUT);

  servo1.attach(servo1pin);
  servo2.attach(servo2pin);
}

void loop() {
  if(Serial.available() > 0) {
    String s = Serial.readStringUntil('\n');
    s.trim();
    Serial.println("=== " + s);

    String mode = s;

    // Update motor speed
    analogWrite(motorSpeedPin, speed);

    if(mode == "left" || mode == "right") {
      // Rotating

      // Rotating commands
      if(mode == "left") {
        angle -= ROTATION_SPEED;
        angle = max(-MAX_ROTATION, angle);
      } else if(mode == "right") {
        angle += ROTATION_SPEED;
        angle = min(MAX_ROTATION, angle);
      }
    } else {
      // Not rotating

      // Move the wheels back towards straight if not already
      if(abs(angle) < ROTATION_BRAKING) {
        angle = 0;
      } else {
        angle += ROTATION_BRAKING * (angle < 0 ? 1 : -1);
      }

      // Movement commands
      if(mode == "forward") {
        digitalWrite(motor1pin1, HIGH);
        digitalWrite(motor1pin2, LOW);
      } else if(mode == "backward") {
        digitalWrite(motor1pin1, LOW);
        digitalWrite(motor1pin2, HIGH);
      } else if(mode == "stop") {
        digitalWrite(motor1pin1, LOW);
        digitalWrite(motor1pin2, LOW);
      } else if(mode == "slow") {
        speed = 100;
        analogWrite(9, speed);
      } else if(mode == "medium") {
        speed = 255;
        analogWrite(9, speed);
      }
    }

    // Update the wheel angle
    // Each servo rotates in opposite directions
    servo1.write(90 + angle);
    servo2.write(90 - angle);
  }
}


// Old stuff

//Controlling speed (0  = off and 255 = max speed):     
//(Optional)
/*analogWrite(9, 100); //ENA  pin
analogWrite(10, 200); //ENB pin
//(Optional)

digitalWrite(motor1pin1,  HIGH);
digitalWrite(motor1pin2, LOW);

digitalWrite(motor2pin1, HIGH);
digitalWrite(motor2pin2, LOW);
delay(3000);

digitalWrite(motor1pin1,  LOW);
digitalWrite(motor1pin2, HIGH);

digitalWrite(motor2pin1, LOW);
digitalWrite(motor2pin2, HIGH);
delay(3000);*/