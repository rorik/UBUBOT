#include <Wire.h>
#include <SoftwareSerial.h>
#include <stdlib.h>
#include "MeOrion.h"

#define DEBUG_MODE true
#define ERROR(message) Serial.println(message);
#define ERROR_CONTEXT(message, context) Serial.print(message); Serial.print(" ("); Serial.print(context); Serial.println(')');

#define LEFT_RATIO -1.0
#define RIGHT_RATIO 1.0
#define SERIAL_RATE 38400

#define START_CHAR '{'
#define END_CHAR '}'
#define SEPARATOR ';'
#define MAX_LENGHT 100
#define MAX_SECTIONS 10

#define LEFT_MOTOR 'L'
#define RIGHT_MOTOR 'R'
#define BOTH_MOTORS 'B'

#define UNDEFINED -1

const MeEncoderMotor motor_left(0x09, SLOT2);
const MeEncoderMotor motor_right(0x09, SLOT1);

char input_buffer[MAX_LENGHT];
int buffer_position = UNDEFINED;

void setup() {
  motor_left.begin();
  motor_right.begin();
  stop();
  Serial.begin(SERIAL_RATE);
}

void loop() {
  if (Serial.available() > 0) {
    int received = Serial.read();
    if (received == START_CHAR) {
      buffer_position = 0;
    } else if(received == END_CHAR && buffer_position != UNDEFINED) {
      if (buffer_position < MAX_LENGHT - 1) {
        input_buffer[buffer_position] = '\0';
      }
      buffer_position = UNDEFINED;
      process_command(input_buffer);
      input_buffer[0] = '\0';
    } else if (buffer_position != UNDEFINED) {
      if (buffer_position >= MAX_LENGHT) {
        buffer_position = UNDEFINED;
        ERROR("Input buffer overflow");
      } else {
        input_buffer[buffer_position++] = received;
      }
    }
  }
}

void process_command(char command[]) {
  //Serial.println(command);
  char sections[MAX_SECTIONS][MAX_LENGHT];
  int section_count = 1;
  for(int i = 0, position = 0; section_count <= MAX_SECTIONS;) {
    if (command[i] == SEPARATOR) {
      sections[section_count++ - 1][position] = '\0';
      position = 0;
    } else {
      sections[section_count - 1][position++] = command[i];
    }
    if (++i >= MAX_LENGHT || command[i] == '\0') {
      sections[section_count - 1][position] = '\0';
      break;
    }
  }

  #if DEBUG_MODE
    Serial.print(sections[0]);
    Serial.print("(");
    if (section_count > 1) {
      for(int i = 1; i < section_count - 1; i++) {
        Serial.print(sections[i]);
        Serial.print(", ");
      }
      Serial.print(sections[section_count - 1]);
    }
    Serial.println(")");
  #endif

  if (strcmp(sections[0], "RUN") == 0) {
    if (section_count == 1 || section_count > 4 || sections[1][1] != '\0') {
      ERROR("Invalid RUN parameters");
    } else if (section_count == 3) {
      run(sections[1][0], atof(sections[2]));
    } else {
      run_for(sections[1][0], atof(sections[2]), atof(sections[3]));
    }
  } else if (strcmp(sections[0], "MOVB") == 0) {
    if (section_count != 4 || sections[1][1] != '\0') {
      ERROR("Invalid MOVB parameters");
    } else {
      move_by(sections[1][0], atof(sections[2]), atof(sections[3]));
    }
  } else if (strcmp(sections[0], "MOVT") == 0) {
    if (section_count != 4 || sections[1][1] != '\0') {
      ERROR("Invalid MOVT parameters");
    } else {
      move_to(sections[1][0], atof(sections[2]), atof(sections[3]));
    }
  } else if (strcmp(sections[0], "STOP") == 0) {
    stop();
  } else {
    ERROR_CONTEXT("Unknown command", sections[0]);
  }
}

void run(char motor, float speed) {
  #if DEBUG_MODE
    Serial.print('[');
    Serial.print(motor);
    Serial.print("]  Speed = ");
    Serial.println(speed);
  #endif
  switch (motor)
  {
    case LEFT_MOTOR:
      motor_left.runSpeed(speed * LEFT_RATIO);
      break;
    case RIGHT_MOTOR:
      motor_right.runSpeed(speed * RIGHT_RATIO);
      break;
    case BOTH_MOTORS:
      motor_left.runSpeed(speed * LEFT_RATIO);
      motor_right.runSpeed(speed * RIGHT_RATIO);
      break;
    default:
      ERROR_CONTEXT("Invalid motor identifier", motor);
      break;
  }
}

void run_for(char motor, float speed, float seconds) {
  #if DEBUG_MODE
    Serial.print('[');
    Serial.print(motor);
    Serial.print("]  Speed = ");
    Serial.print(speed);
    Serial.print(", Duration = ");
    Serial.println(seconds);
  #endif
  switch (motor)
  {
    case LEFT_MOTOR:
      motor_left.runSpeedAndTime(speed * LEFT_RATIO, seconds);
      break;
    case RIGHT_MOTOR:
      motor_right.runSpeedAndTime(speed * RIGHT_RATIO, seconds);
      break;
    case BOTH_MOTORS:
      motor_left.runSpeedAndTime(speed * LEFT_RATIO, seconds);
      motor_right.runSpeedAndTime(speed * RIGHT_RATIO, seconds);
      break;
    default:
      ERROR_CONTEXT("Invalid motor identifier", motor);
      break;
  }
}

void move_by(char motor, float angle, float speed) {
  #if DEBUG_MODE
    Serial.print('[');
    Serial.print(motor);
    Serial.print("]  Angle = ");
    Serial.print(angle);
    Serial.print(", Speed = ");
    Serial.println(speed);
  #endif
  switch (motor)
  {
    case LEFT_MOTOR:
      Serial.println("A");
      motor_left.move(angle, speed);
      Serial.println("B");
      break;
    case RIGHT_MOTOR:
      Serial.println("A");
      motor_right.move(angle, speed);
      Serial.println("B");
      break;
    case BOTH_MOTORS:
      Serial.println("A");
      motor_left.move(angle, speed);
      motor_right.move(angle, speed);
      Serial.println("B");
      break;
    default:
      ERROR_CONTEXT("Invalid motor identifier", motor);
      break;
  }
}

void move_to(char motor, float angle, float speed) {
  #if DEBUG_MODE
    Serial.print('[');
    Serial.print(motor);
    Serial.print("]  Angle = ");
    Serial.print(angle);
    Serial.print(", Speed = ");
    Serial.println(speed);
  #endif
  switch (motor)
  {
    case LEFT_MOTOR:
      motor_left.moveTo(angle, speed);
      break;
    case RIGHT_MOTOR:
      motor_right.moveTo(angle, speed);
      break;
    case BOTH_MOTORS:
      motor_left.moveTo(angle, speed);
      motor_right.moveTo(angle, speed);
      break;
    default:
      ERROR_CONTEXT("Invalid motor identifier", motor);
      break;
  }
}

void stop() {
  move_by(BOTH_MOTORS, 0, 0);
}