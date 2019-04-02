#include <wiringPi.h>
#include "channels.h"

int main(void)
{
    wiringPiSetup();
    digitalWrite(LEFT_CHANNEL, LOW);
    digitalWrite(RIGHT_CHANNEL, LOW);
    return 0;
}