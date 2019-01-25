#include <Wire.h>
#include <NewPing.h>

#define SERIAL_DISABLED
#define SLAVE_ADDRESS 0x10
#define HANDSHAKE 123
#define IR_COUNT 2
#define US_MAX_DISTANCE 400
#define US_COUNT 1
#define US_DELAY 33
#define COM 13
#define US_NW_E 12
#define US_NW_T 11
#define US_N_E 10
#define US_N_T 9
#define US_NE_E 8
#define US_NE_T 7
#define IR_N 3
#define IR_S 2

byte output;
bool enableInterrupts = true;
char handshakeSelected = -1;

bool IRTriggered[IR_COUNT] = {false, false};

unsigned long pingTimer[US_COUNT];
unsigned int cm[US_COUNT];
unsigned int lastDistance[US_COUNT] = {-1, -1, -1};
uint8_t currentSensor = 0;

NewPing sonar[US_COUNT] = {
  //NewPing(US_NW_T, US_NW_E, US_MAX_DISTANCE),
  NewPing(US_N_T, US_N_E, US_MAX_DISTANCE),
  //NewPing(US_NE_T, US_NE_E, US_MAX_DISTANCE)
};


void setup() {
  #ifdef SERIAL_ENABLED
  Serial.begin(9600);
  #endif
  pingTimer[0] = millis() + 75;
  for (uint8_t i = 1; i < US_COUNT; i++) // Set the starting time for each sensor.
    pingTimer[i] = pingTimer[i - 1] + US_DELAY;
  pinMode(COM, OUTPUT);
  pinMode(IR_N, INPUT_PULLUP);
  pinMode(IR_S, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(IR_N), infraredInterruptNR, RISING);
  attachInterrupt(digitalPinToInterrupt(IR_S), infraredInterruptSR, RISING);
  attachInterrupt(digitalPinToInterrupt(IR_N), infraredInterruptNF, FALLING);
  attachInterrupt(digitalPinToInterrupt(IR_S), infraredInterruptSF, FALLING);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(dataRequest);
  Wire.onRequest(dataOutput);
}

void loop() {
  for (uint8_t i = 0; i < US_COUNT; i++) { // Loop through all the sensors.
    if (millis() >= pingTimer[i]) {         // Is it this sensor's time to ping?
      pingTimer[i] += US_DELAY * US_COUNT;  // Set next time this sensor will be pinged.
      sonar[currentSensor].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
      currentSensor = i;                          // Sensor being accessed.
      cm[currentSensor] = 0;                      // Make distance zero in case there's no ping echo for this sensor.
      sonar[currentSensor].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
    }
  }
}

void echoCheck() { // If ping received, set the sensor distance to array.
  if (sonar[currentSensor].check_timer()) {
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
    pingResult(currentSensor);
  }
}

void pingResult(uint8_t sensor) { // Sensor got a ping, do something with the result.
  #ifdef SERIAL_ENABLED
  Serial.print(sensor);
  Serial.print(" = ");
  Serial.print(cm[sensor]);
  Serial.println(" cm");
  #endif
  lastDistance[sensor] = cm[sensor];
}

void interrupt(bool state) {
  if (enableInterrupts) {
    digitalWrite(COM, state);
  }
}

void infraredInterruptNR() {
  IRTriggered[0] = true;
  interrupt(HIGH);
}

void infraredInterruptNF() {
  IRTriggered[0] = false;
  interrupt(LOW);
}

void infraredInterruptSR() {
  IRTriggered[1] = true;
  interrupt(HIGH);
}

void infraredInterruptSF() {
  IRTriggered[1] = false;
  interrupt(LOW);
}

void dataRequest(int byteCount) {
  while(Wire.available()) {
    byte request = Wire.read();
    #ifdef SERIAL_ENABLED
      printRequest(request);
    #endif
    if (request < 128) {
      if (request < US_COUNT * 3) {
        output = lastDistance[request%US_COUNT] / (request / US_COUNT + 1);
        if (output > 126)
          output = 126;
      }
      else if (request > 19 && request < 50) {
        #if(US_COUNT + IR_COUNT <= 7)
          output = 0;
          unsigned char threshold = request - 20;
          for (int i = 0; i < US_COUNT; i++)
            if (lastDistance[i] <= threshold)
              output += 1<<i;
          for (int i = 0; i < IR_COUNT; i++)
            if (IRTriggered[i])
              output += 1<<(7-i);
        #else
          output = 127;
        #endif
      }
      else if (request > 49 && request < 54) {
        if (request != 53)
          enableInterrupts = request == 52 ? ! enableInterrupts : request == 51;
        output = enableInterrupts;
      }
      else if (request == handshakeSelected) {
        output = HANDSHAKE;
        handshakeSelected = -1;
      }
      else if (request == HANDSHAKE) {
        output = handshakeSelected = random(100, 109);
      }
      else output = 127;
    } else {
      if (request > 129 && request < 130 + US_COUNT * 4) {
        int temp = lastDistance[(request - 130)%US_COUNT] - 254*((request - 130)/ US_COUNT);
        output = temp < 0 ? 0 : (temp > 254 ? 254 : temp);
      }
      else output = 255;
    }
  }
}

void dataOutput() {
  Wire.write(output);
  #ifdef SERIAL_ENABLED
    Serial.print("> ");
    printRequest(output);
  #endif
}

void printRequest(byte myByte){
  Serial.print(myByte);
  Serial.print(" = B");
  for(byte mask = 0x80; mask; mask >>= 1){
    if(mask  & myByte)
      Serial.print('1');
    else
      Serial.print('0');
  }
  Serial.println();
}
