#include <Wire.h>
#include "comms.h"

/* Debug Config */
#define DEBUG_MODE true
#define ERROR(message) Serial.println(message);
#define ERROR_CONTEXT(message, context) Serial.print(message); Serial.print(" ("); Serial.print(context); Serial.println(')');

/* Speed Config */
#define LEFT_RATIO   -1.0
#define RIGHT_RATIO  1.0
#define MAX_SPEED    200

/* Serial Config */
#define SERIAL_RATE    230400
#define START_CHAR     '{'
#define END_CHAR       '}'
#define CHECKSUM_CHAR  '$'
#define SEPARATOR      ';'
#define LEFT_MOTOR     'L'
#define RIGHT_MOTOR    'R'
#define BOTH_MOTORS    'B'
#define MAX_LENGHT     100
#define MAX_SECTIONS   10
#define MAX_RETRIES    5

/* Serial Commands */
#define COMMAND_MOVB  "MOVB"
#define COMMAND_MOVT  "MOVT"
#define COMMAND_STOP  "STOP"
#define COMMAND_RUN   "RUN"
#define COMMAND_RUNF  "RNF"
#define COMMAND_POS   "POS"
#define COMMAND_SPD   "SPD"
#define COMMAND_ERR   "?E"
#define COMMAND_UPTM  "?U"

/* Encoder Config */
#define LEFT_SLOT   1
#define RIGHT_SLOT  0
#define ADDRESS     0x9

/* Internal Constants */
#define UNDEFINED       -1
#define NULL_EXECUTION  { .function = NOP }

/* Type Definitions */
typedef enum function_type { NOP, RUN, RUNF, MOVB, MOVT, POS, SPD } Function;
typedef struct execution {
  Function function;
  char motor;
  float args[2];
} Execution;

/* Function Declarations */
Execution process_command(char *command);
void execute(Execution ex);
bool execute_movement(Execution ex, bool (*function)(uint8_t, float, float));
void print_info(char motor, float (*function)(uint8_t));
bool run(uint8_t slot, float speed);
bool run_for(uint8_t slot, float speed, float time);
bool move_by(uint8_t slot, float speed, float angle);
bool move_to(uint8_t slot, float speed, float angle);
bool move(uint8_t function, uint8_t slot, float speed, float angle);
float speed(uint8_t slot);
float position(uint8_t slot);
float get_info(uint8_t function, uint8_t slot);
bool reset_motor(uint8_t slot);
float normalize_speed(float speed);

/* Serial Variables */
char input_buffer[MAX_LENGHT];
int8_t buffer_position = UNDEFINED;
uint32_t checksum;
bool is_checksum = false;

/* Execution Variables */
Execution current_execution = NULL_EXECUTION;
uint32_t failed_executions = 0;


void setup() {
	Serial.begin(SERIAL_RATE);
  #if DEBUG_MODE
    Serial.println("Started");
  #endif
  Wire.begin();
  reset_motor(LEFT_SLOT);
  reset_motor(RIGHT_SLOT);
}

void loop() {
  for(uint8_t i = MAX_RETRIES; current_execution.function != NOP && i > 0 ; i--) {
    failed_executions++;
    #if DEBUG_MODE
      ERROR("!> 00 - Previous execution did not succeed");
    #endif
    execute(current_execution);
  }
  
  while (!Serial.available())
    continue;
  
  do {
    char received = Serial.read();
    if (received == START_CHAR) {
      buffer_position = 0;
      checksum = 0;
    } else if(received == END_CHAR && buffer_position != UNDEFINED) {
      if (buffer_position < MAX_LENGHT - 1) {
        input_buffer[buffer_position] = '\0';
      }
      is_checksum = false;
      buffer_position = UNDEFINED;
      Execution ex = process_command(input_buffer);
      input_buffer[0] = '\0';
      if (ex.function != NOP) {
        execute(ex);
      }
      return;
    } else if(received == CHECKSUM_CHAR && buffer_position != UNDEFINED) {
      is_checksum = true;
    } else if (buffer_position != UNDEFINED) {
      if (is_checksum) {
        if ((checksum % 10) != (received - 48)) {
          is_checksum = false;
          buffer_position = UNDEFINED;
          ERROR_CONTEXT("!> 10 - Checksum validation failed", checksum % 10);
        }
      } else if (buffer_position >= MAX_LENGHT) {
        buffer_position = UNDEFINED;
        is_checksum = false;
        ERROR("!> 20 - Input buffer overflow");
      } else {
        input_buffer[buffer_position++] = received;
        checksum += received;
      }
    }
  } while (Serial.available());
}

Execution process_command(char *command) {
  char sections[MAX_SECTIONS][MAX_LENGHT];
  uint8_t section_count = 1;
  for(uint8_t i = 0, position = 0; section_count <= MAX_SECTIONS;) {
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
      for(uint8_t i = 1; i < section_count - 1; i++) {
        Serial.print(sections[i]);
        Serial.print(", ");
      }
      Serial.print(sections[section_count - 1]);
    }
    Serial.println(')');
  #endif

  size_t command_lenght = strlen(sections[0]);
  /* MOVB, MOVT, STOP*/
  if (command_lenght == 4) {
    if (strncmp(sections[0], COMMAND_MOVB, 3) == 0) {
      if (section_count != 4 || sections[1][1] != '\0') {
          ERROR("!> 40 - Invalid MOVB/MOVT parameters");
          return NULL_EXECUTION;
      }
      Execution ex = { .function = MOVB, .motor = sections[1][0], .args = { (float)atof(sections[2]), (float)atof(sections[3]) } };
      if (sections[0][3] == COMMAND_MOVB[3]) {
        return ex;
      } else if (sections[0][3] == COMMAND_MOVT[3]) {
        ex.function = MOVT;
        return ex;
      }
    } else if (strcmp(sections[0], COMMAND_STOP) == 0) {
      return { .function = RUN, .motor = BOTH_MOTORS, .args = { 0 } };
    }
  /* RUN, RUNF, POS, SPD */
  } else if (command_lenght == 3) {
    if (sections[0][0] == COMMAND_RUN[0]) {
      if (strcmp(sections[0], COMMAND_RUNF) == 0) {
        if (section_count != 4 || sections[1][1] != '\0') {
            ERROR("!> 41 - Invalid RUNF parameters");
            return NULL_EXECUTION;
        } else {
          return { .function = RUNF, .motor = sections[1][0], .args = { (float)atof(sections[2]), (float)atof(sections[3]) } };
        }
      } else if (strcmp(sections[0], COMMAND_RUN) == 0) {
        if (section_count != 3 || sections[1][1] != '\0') {
            ERROR("!> 42 - Invalid RUN parameters");
            return NULL_EXECUTION;
        } else {
          return { .function = RUN, .motor = sections[1][0], .args = { (float)atof(sections[2]) } };
        }
      }
    } else if (strcmp(sections[0], COMMAND_POS) == 0) {
      if (section_count != 2 || sections[1][1] != '\0') {
          ERROR("!> 43 - Invalid POS parameters");
          return NULL_EXECUTION;
      } else {
        return { .function = POS, .motor = sections[1][0] };
      }
    } else if (strcmp(sections[0], COMMAND_SPD) == 0) {
      if (section_count != 2 || sections[1][1] != '\0') {
          ERROR("!> 44 - Invalid SPD parameters");
          return NULL_EXECUTION;
      } else {
        return { .function = SPD, .motor = sections[1][0] };
      }
    }
  /* ERR, UPTM */
  } else if (command_lenght == 2 && sections[0][0] == COMMAND_ERR[0]) {
    if (sections[0][1] == COMMAND_ERR[1]) {
      Serial.print(">> ");
      Serial.print(failed_executions);
      Serial.println(" <<");
      return NULL_EXECUTION;
    } else if (sections[0][1] == COMMAND_UPTM[1]) {
      Serial.print(">> ");
      Serial.print(millis());
      Serial.println(" <<");
      return NULL_EXECUTION;
    }
  }
  
  ERROR_CONTEXT("!> 30 - Unknown command", sections[0]);
  return NULL_EXECUTION;
}

void execute(Execution ex) {
  current_execution = ex;
  if (ex.motor != BOTH_MOTORS && ex.motor != LEFT_MOTOR && ex.motor != RIGHT_MOTOR) {
    ERROR_CONTEXT("!> 51 - Invalid motor identifier", ex.function);
    current_execution = NULL_EXECUTION;
    return;
  }

  bool ack = UNDEFINED;
  switch (ex.function) {
    case MOVB:
      ack = execute_movement(ex, move_by);
      break;
    case MOVT:
      ack = execute_movement(ex, move_to);
      break;
    case RUNF:
      ack = execute_movement(ex, run_for);
      break;
    case RUN:
      if (ex.motor == BOTH_MOTORS) {
        ack = run(LEFT_SLOT, ex.args[0] * LEFT_RATIO);
        ack &= run(RIGHT_SLOT, ex.args[0] * RIGHT_RATIO);
      } else if (ex.motor == LEFT_MOTOR) {
        ack = run(LEFT_SLOT, ex.args[0] * LEFT_RATIO);
      } else {
        ack = run(RIGHT_SLOT, ex.args[0] * RIGHT_RATIO);
      }
      break;
    case POS:
      print_info(ex.motor, position);
      current_execution = NULL_EXECUTION;
      return;
    case SPD:
      print_info(ex.motor, speed);
      current_execution = NULL_EXECUTION;
      return;
    default:
      ERROR_CONTEXT("!> 50 - Invalid execute function", ex.function);
      current_execution = NULL_EXECUTION;
      return;
  }

  #if DEBUG_MODE
    Serial.print(ex.function);
    Serial.print(" =ack=> ");
    Serial.println(ack);
  #endif

  current_execution = NULL_EXECUTION;
}

bool execute_movement(Execution ex, bool (*function)(uint8_t, float, float)) {
  if (ex.motor == BOTH_MOTORS) {
    return (*function)(LEFT_SLOT, ex.args[0] * LEFT_RATIO, ex.args[1]) &
      (*function)(RIGHT_SLOT, ex.args[0] * RIGHT_RATIO, ex.args[1]);
  } else if (ex.motor == LEFT_MOTOR) {
    return (*function)(LEFT_SLOT, ex.args[0] * LEFT_RATIO, ex.args[1]);
  } else {
    return (*function)(RIGHT_SLOT, ex.args[0] * RIGHT_RATIO, ex.args[1]);
  }
}

void print_info(char motor, float (*function)(uint8_t)) {
  if (motor == BOTH_MOTORS) {
    float info_L = (*function)(LEFT_SLOT);
    float info_R = (*function)(RIGHT_SLOT);
    Serial.print(">> L = ");
    Serial.print(info_L);
    Serial.print(" , R = ");
    Serial.print(info_R);
    Serial.println(" <<");
  } else if (motor == LEFT_MOTOR) {
    float info = (*function)(LEFT_SLOT);
    Serial.print(">> L = ");
    Serial.print(info);
    Serial.println(" <<");
  } else {
    float info = (*function)(RIGHT_SLOT);
    Serial.print(">> R = ");
    Serial.print(info);
    Serial.println(" <<");
  }
}

bool run(uint8_t slot, float speed) {
  uint8_t buffer[14] = {0};
  uint8_t response[10] = {0};

  uint8_t data[6] = {0};
  data[0] = slot;
  data[1] = ENCODER_MOTOR_RUN_STOP;
  *((float *)(data + 2)) = normalize_speed(speed);

  pack(buffer, 14, 0x01, data, 6);
  request(buffer, response, 14, 10);
  pushStr(response, 10);
  send();

  return 0;
}

bool run_for(uint8_t slot, float speed, float time) {
  uint8_t buffer[18] = {0};
  uint8_t response[10] = {0};

  uint8_t data[10] = {0};
  data[0] = slot;
  data[1] = ENCODER_MOTOR_SPEED_TIME;
  *((float *)(data + 2)) = normalize_speed(speed);
  *((float *)(data + 6)) = time;

  pack(buffer, 18, 0x01, data, 10);
  request(buffer, response, 18, 10);
  pushStr(response, 10);
  send();

  return 0;
}

bool move_by(uint8_t slot, float speed, float angle) {
  return move(ENCODER_MOTOR_MOVE, slot, angle, speed);
}

bool move_to(uint8_t slot, float speed, float angle) {
  return move(ENCODER_MOTOR_MOVE_TO, slot, angle, speed);
}

bool move(uint8_t function, uint8_t slot, float speed, float angle) {
  uint8_t buffer[18] = {0};
  uint8_t response[10] = {0};

  uint8_t data[10] = {0};
  data[0] = slot;
  data[1] = function;
  *((float *)(data + 2)) = angle; // 2 - 5
  *((float *)(data + 6)) = normalize_speed(speed); // 6 - 9

  pack(buffer, 18, 0x01, data, 10);
  request(buffer, response, 18, 10);
  pushStr(response, 10);
  send();

  uint8_t ack[2] = {0};
  getData(ack, 2);
  return ack[1];
}

float speed(uint8_t slot) {
  return get_info(ENCODER_MOTOR_GET_SPEED, slot);
}

float position(uint8_t slot) {
  return get_info(ENCODER_MOTOR_GET_POS, slot);
}

float get_info(uint8_t function, uint8_t slot) {
  uint8_t buffer[10] = {0};
  uint8_t response[14] = {0};
  
  uint8_t data[] = {slot, function};

  pack(buffer, 10, 0x01, data, 2);
  request(buffer, response, 10, 14);
  pushStr(response, 14);
  send();

  uint8_t result[6] = {0};
  getData(result, 6);
  return *((float *)(result + 2));
}

bool reset_motor(uint8_t slot) {
  uint8_t buffer[10] = {0};
  uint8_t response[10] = {0};
  
  uint8_t data[] = {slot, ENCODER_MOTOR_RESET};

  pack(buffer, 10, 0x01, data, 2);
  request(buffer, response, 10, 10);
  pushStr(response, 10);

  uint8_t ack[2] = {0};
  getData(ack, 2);
  return ack[1];
}

float normalize_speed(float speed) {
  if(speed > MAX_SPEED) {
    return MAX_SPEED;
  } else if(speed < -MAX_SPEED) {
    return -MAX_SPEED;
  }
  return speed;
}
