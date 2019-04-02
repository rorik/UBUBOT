#include <wiringPi.h>
#include <softTone.h>
#include <stdio.h>
#include <math.h>
#include "channels.h"

int main(void)
{
    wiringPiSetup();
    softToneCreate(LEFT_CHANNEL);
    softToneCreate(RIGHT_CHANNEL);
    for (int i = 20; i < 260; i++)
    {
        softToneWrite(LEFT_CHANNEL, i * 5);
        softToneWrite(RIGHT_CHANNEL, i * 6);
        delay(8);
    }
    delay(5000);

    softToneWrite(LEFT_CHANNEL, LOW);
    softToneWrite(RIGHT_CHANNEL, LOW);
    return 0;
}