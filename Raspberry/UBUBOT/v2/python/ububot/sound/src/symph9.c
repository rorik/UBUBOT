#include <wiringPi.h>
#include <softTone.h>
#include <stdio.h>
#include "tones.h"
#include "channels.h"

const int bpm = 120 / 4;
const int sequence[] = {E4, E4, F4, G4, G4, F4, E4, D4, C4, C4, D4, E4, E4, D4, D4, E4, E4, F4, G4, G4, F4, E4, D4, C4, C4, D4, E4,    D4, C4, C4};
const float beats[] =  {QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, EN, HN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN, QN DT, EN, HN};
const int length = sizeof(sequence) / sizeof(int);

int main(void)
{
    wiringPiSetup();
    softToneCreate(LEFT_CHANNEL);
    for (int i = 0; i < length; i++)
    {
        softToneWrite(LEFT_CHANNEL, sequence[i]);
        delay(60000 / bpm * beats[i] - 8);
        softToneWrite(LEFT_CHANNEL, LOW);
        delay(8);
    }
    softToneWrite(LEFT_CHANNEL, LOW);
    return 0;
}