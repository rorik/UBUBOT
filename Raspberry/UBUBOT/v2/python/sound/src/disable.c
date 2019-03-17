#include <wiringPi.h>
#include "channels.h"

int main(void)
{
    wiringPiSetup();
    pinMode(ENABLE_CHANNEL, OUTPUT);
    digitalWrite(ENABLE_CHANNEL, HIGH);
    return 0;
}