#include <wiringPi.h>
#include "channels.h"

int main(void)
{
    wiringPiSetup();
    pinMode(ENABLE_CHANNEL, OUTPUT);
    digitalWrite(ENABLE_CHANNEL, HIGH);
    digitalWrite(LEFT_CHANNEL, LOW);
    digitalWrite(RIGHT_CHANNEL, LOW);
    return 0;
}