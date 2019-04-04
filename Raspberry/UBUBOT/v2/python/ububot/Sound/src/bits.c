#include <wiringPi.h>
#include <softTone.h>
#include <stdio.h>
#include "tones.h"
#include "channels.h"

#if SONG == 1
/* Windows XP start up - Arranged by about@rorik.me */
const int sequenceR[] = {E5F, E4F, B4F  , A4F, E5F, B4F  };
const int sequenceL[] = {RR , RR , RR   , RR , RR , RR   };
const float beats[] =   {EN , SN , EN DT, QN , EN , QN DT};
const int bpm = 120 / 4;
#elif SONG == 2
/* Windows XP shut down - Arranged by about@rorik.me */
const int sequenceR[] = {A5F, E5F, A4F, B4F};
const int sequenceL[] = {RR , RR , RR , RR };
const float beats[] =   {EN , EN , EN , HN };
const int bpm = 120 / 4;
#else
const int bpm = 0;
const int sequenceR[] = {};
const int sequenceL[] = {};
const float beats[] = {};
#endif

#ifndef SPACING
#define SPACING 8
#endif

const int length = sizeof(beats) / sizeof(int);

int main(void)
{
    if (length >= 0 && bpm > 0)
    {
        wiringPiSetup();
        softToneCreate(LEFT_CHANNEL);
        softToneCreate(RIGHT_CHANNEL);
        for (int i = 0; i < length; i++)
        {
            if (sequenceR[i] != SS)
            {
                softToneWrite(RIGHT_CHANNEL, sequenceR[i]);
            }
            if (sequenceL[i] != SS)
            {
                softToneWrite(LEFT_CHANNEL, sequenceL[i]);
            }
            delay(60000 / bpm * beats[i] - SPACING);
            if (sequenceR[i + 1] != SS)
            {
                softToneWrite(RIGHT_CHANNEL, LOW);
            }
            if (sequenceL[i + 1] != SS)
            {
                softToneWrite(LEFT_CHANNEL, LOW);
            }
            delay(SPACING);
        };
        digitalWrite(LEFT_CHANNEL, LOW);
        digitalWrite(RIGHT_CHANNEL, LOW);
    }
    return 0;
}
