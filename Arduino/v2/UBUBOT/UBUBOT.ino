#include <Wire.h>
#include <SoftwareSerial.h>
#include <stdlib.h>
#include "MeOrion.h"

#define DEBUG_MODE true
#define ERROR(message) Serial.println(message);
#define ERROR_CONTEXT(message, context) Serial.print(message); Serial.print(" ("); Serial.print(context); Serial.println(')');

#define LEFT_RATIO -1.0
#define RIGHT_RATIO 1.0
#define SERIAL_RATE 115200

#define START_CHAR '{'
#define END_CHAR '}'
#define CHECKSUM_CHAR '$'
#define SEPARATOR ';'
#define MAX_LENGHT 100
#define MAX_SECTIONS 10

#define LEFT_MOTOR 'L'
#define RIGHT_MOTOR 'R'
#define BOTH_MOTORS 'B'

#define UNDEFINED -1

typedef enum function_type {RUN, RUNF, MOVB, MOVT, STOP, NOP} Function;
/*typedef struct execution {
  Function function;
  char motor;
  float args[2];
} Execution;*/

const MeEncoderMotor motor_left(0x09, SLOT2);
const MeEncoderMotor motor_right(0x09, SLOT1);

char input_buffer[MAX_LENGHT];
int buffer_position = UNDEFINED;
int checksum;
bool is_checksum = false;
Function function;
char motor;
float args[2];

void setup() {
  motor_left.begin();
  motor_right.begin();
  stop();
  Serial.begin(SERIAL_RATE);
}

void loop() {
  /*if (current_execution != NULL) {
    //execute(*current_execution);
  }*/
  if (Serial.available() > 0) {
    int received = Serial.read();
    if (received == START_CHAR) {
      buffer_position = 0;
      checksum = 0;
    } else if(received == END_CHAR && buffer_position != UNDEFINED) {
      if (buffer_position < MAX_LENGHT - 1) {
        input_buffer[buffer_position] = '\0';
      }
      is_checksum = false;
      buffer_position = UNDEFINED;
      process_command(input_buffer);
      input_buffer[0] = '\0';
    } else if(received == CHECKSUM_CHAR && buffer_position != UNDEFINED) {
      is_checksum = true;
    } else if (buffer_position != UNDEFINED) {
      if (is_checksum) {
        if ((checksum % 10) != (received - 48)) {
          is_checksum = false;
          buffer_position = UNDEFINED;
          ERROR_CONTEXT("Checksum validation failed", checksum % 10);
        }
      } else if (buffer_position >= MAX_LENGHT) {
        buffer_position = UNDEFINED;
        is_checksum = false;
        ERROR("Input buffer overflow");
      } else {
        input_buffer[buffer_position++] = received;
        checksum += received;
      }
    }
  }
}

void process_command(char command[]) {
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
    Serial.print('(');
    if (section_count > 1) {
      for(int i = 1; i < section_count - 1; i++) {
        Serial.print(sections[i]);
        Serial.print(", ");
      }
      Serial.print(sections[section_count - 1]);
    }
    Serial.println(')');
  #endif

  if (strcmp(sections[0], "RUN") == 0) {
    Serial.println("WTF - 1");
    if (section_count == 1 || section_count > 4 || sections[1][1] != '\0') {
      ERROR("Invalid RUN parameters");
    } else if (section_count == 3) {
      //current_execution = { .function = RUN, .motor = sections[1][0], .arg1 = atof(sections[2]) };
      //execute();
    } else {
      //current_execution = { .function = RUNF, .motor = sections[1][0], .arg1 = atof(sections[2]), .arg2 = atof(sections[3]) };
      //execute();
    }
  } else if (strcmp(sections[0], "MOVB") == 0) {
    Serial.println("WTF - 2");
    if (section_count != 4 || sections[1][1] != '\0') {
      ERROR("Invalid MOVB parameters");
    } else {
      //current_execution.function = MOVB;
      //current_execution.motor = sections[1][0];
      //current_execution.arg1 = (float)atof(sections[2]);
      //current_execution.args = malloc(2 * sizeof(double));
      //current_execution.args[0] = atof(sections[2]);
      //current_execution.args[1] = atof(sections[3]);
      //current_execution.arg1 = 10.1;
      //Serial.println(current_execution.args[0]);
      //current_execution.arg2 = (float)atof(sections[3]);
      //Execution executions = { .function = MOVB, .motor = sections[1][0], .args = { atof(sections[2]), atof(sections[3]) } };
      function = MOVB;
      motor = sections[1][0];
      args[0] = atof(sections[2]);
      args[1] = atof(sections[3]);
      execute();
    }
  } else if (strcmp(sections[0], "MOVT") == 0) {
    Serial.println("WTF - 3");
    if (section_count != 4 || sections[1][1] != '\0') {
      ERROR("Invalid MOVT parameters");
    } else {
      //current_execution = { .function = MOVT, .motor = sections[1][0], .arg1 = atof(sections[2]), .arg2 = atof(sections[3]) };
      //execute();
    }
  } else if (strcmp(sections[0], "STOP") == 0) {
    Serial.println("STOP!!!!");
    //(&current_execution)->motor = 'X';
    //Serial.println("STOP!!!!?");
    //current_execution = { .function = STOP };
    //execute();
  } else {
    Serial.println("WTF?");
    //current_execution.function = NOP;
    ERROR_CONTEXT("Unknown command", sections[0]);
  }
}

//void executee(Execution execution) {
void execute() {
  Serial.println("Started Execution");
  Serial.println("Switch...");
  if (function == MOVB) {
    Serial.print("move_by(");
    Serial.print(motor);
    Serial.print(", ");
    Serial.print(args[0]);
    Serial.print(", ");
    Serial.print(args[1]);
    Serial.println(')');
    move_by(motor, args[0], args[1]);
  }
  /*
  if (execution.function == MOVB) {
    Serial.print("move_by(");
    Serial.print(execution.motor);
    Serial.print(", ");
    Serial.print((int)execution.args[0]);
    Serial.print(", ");
    Serial.print((int)execution.args[1]);
    Serial.println(')');
    move_by(execution.motor, execution.args[0], execution.args[1]);
  }
  switch (current_execution.function) {
    case RUN:
      Serial.println(current_execution.motor);
      Serial.println(current_execution.arg1);
      run(current_execution.motor, current_execution.arg1);
      break;
    case RUNF:
      Serial.println(current_execution.motor);
      Serial.println(current_execution.arg1);
      Serial.println(current_execution.arg2);
      run_for(current_execution.motor, current_execution.arg1, current_execution.arg2);
      break;
    case MOVB:
      Serial.println(current_execution.motor);
      Serial.println(current_execution.arg1);
      Serial.println(current_execution.arg2);
      move_by(current_execution.motor, current_execution.arg1, current_execution.arg2);
      break;
    case MOVT:
      Serial.println(current_execution.motor);
      Serial.println(current_execution.arg1);
      Serial.println(current_execution.arg2);
      move_to(current_execution.motor, current_execution.arg1, current_execution.arg2);
      break;
    case STOP:
      stop();
      break;
    default:
      ERROR_CONTEXT("Unknown function", current_execution.function);
      break;
  }*/
  Serial.println("Finished Execution");
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
  bool response;
  switch (motor)
  {
    case LEFT_MOTOR:
      response = motor_left.move(angle * LEFT_RATIO, speed);
      break;
    case RIGHT_MOTOR:
      response = motor_right.move(angle * RIGHT_RATIO, speed);
      break;
    case BOTH_MOTORS:
      response = motor_left.move(angle * LEFT_RATIO, speed);
      response &= motor_right.move(angle * RIGHT_RATIO, speed);
      break;
    default:
      ERROR_CONTEXT("Invalid motor identifier", motor);
      break;
  }
  Serial.println(response ? "success": "failed");
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
      motor_left.moveTo(angle * LEFT_RATIO, speed);
      break;
    case RIGHT_MOTOR:
      motor_right.moveTo(angle * RIGHT_RATIO, speed);
      break;
    case BOTH_MOTORS:
      motor_left.moveTo(angle * LEFT_RATIO, speed);
      motor_right.moveTo(angle * RIGHT_RATIO, speed);
      break;
    default:
      ERROR_CONTEXT("Invalid motor identifier", motor);
      break;
  }
}

void stop() {
  move_by(BOTH_MOTORS, 0, 0);
}
