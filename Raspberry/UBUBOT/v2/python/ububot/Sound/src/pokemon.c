#include <wiringPi.h>
#include <softTone.h>
#include <stdio.h>
#include "tones.h"
#include "channels.h"

#if SONG == 1
/* Battle! (Wild Pokémon) (Red & Blue) - Composed by Junichi Masuda - Arranged by about@rorik.me */
//                       1                                                                          2                                                                       3                               4                               5                                      6                                      7                               8                               9                                      10                                     11                                                                     12                                                                     13
const int sequenceR[] = {G5, G5F, F5 , G6, G5 , G5F, F5 , G6, G5 , G5F, F5 , G6, G5 , G5F, F5, G6 , G5, G5F, F5, G6 , G5, G5F, F5, G6, G5, G5F, F5 , G6, G5 , G5F, F5, G6 , G5, SS, RR, G4, SS, RR, G4, SS, RR, RR, RR, RR, G4, SS, RR, RR, RR , RR , RR , G4 , SS , RR , G4 , SS, RR , RR , RR , F4S, SS , SS , SS , SS, G4, SS, RR, G4, SS, RR, G4, SS, RR, RR, RR, RR, G4, SS, RR, RR, RR , RR , RR , G4 , SS , RR , G4 , SS, RR , RR , RR , G4 , SS , SS , RR , RR, G4 , SS, SS , SS, SS , SS, F4S, SS, SS , SS, SS , SS, E4F, SS, SS, SS, G4, SS , SS, SS , SS, SS , A4, SS , SS, SS , SS, SS, G4, SS , SS, SS , A5F, SS , SS, SS, SS , SS, SS , SS, SS , SS, SS , SS, G5, SS , RR, RR ,  };
const int sequenceL[] = {C5, B4 , B4F, A4, B4F, A4 , A4F, G4, A4F, G4 , G4F, F4, G4F, F4 , E4, E4F, E4, E4F, D4, D4F, D4, D4F, C4, B3, C4, B3 , B3F, A3, A3S, B3 , C4, C4S, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, D3F, A3F, D3F, D3F, A3F, B3F, A3F, G3, D3F, A3F, D3F, D3F, A3F, B3F, A3F, F3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, C3, G3, D3F, A3F, D3F, D3F, A3F, B3F, A3F, G3, D3F, A3F, D3F, D3F, A3F, B3F, A3F, F3, D4F, D4, D4F, C4, D4F, D4, D4F, C4, D4F, D4, E4F, D4, D4 , C4, B3, C4, D4, E4F, D4, C4S, D4, E4F, D4, C4S, D4, E4F, E4, F4, E4, E4F, D4, C4S, D4 , D4S, E4, F4, F4S, G4, G4S, A4, A4F, G4, G4F, F4, E4, E4F, D4, D4F,  };
const float beats[] =   {SN, SN , SN , SN, SN , SN , SN , SN, SN , SN , SN , SN, SN , SN , SN, SN , SN, SN , SN, SN , SN, SN , SN, SN, SN, SN , SN , SN, SN , SN , SN, SN , EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN , EN , EN , EN , EN , EN , EN , EN, EN , EN , EN , EN , EN , EN , EN , EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN , EN , EN , EN , EN , EN , EN , EN, EN , EN , EN , EN , EN , EN , EN , EN, SN , SN, SN , SN, SN , SN, SN , SN, SN , SN, SN , SN, SN , SN, SN, SN, SN, SN , SN, SN , SN, SN , SN, SN , SN, SN , SN, SN, SN, SN , SN, SN , SN , SN , SN, SN, SN , SN, SN , SN, SN , SN, SN , SN, SN, SN , SN, SN ,  };
const int bpm = 180 / 4;
#elif SONG == 2
/* Battle! (Wild Pokémon) (Ruby & Shapphire) - Composed by Junichi Masuda - Arranged by about@rorik.me */
const int sequenceR[] = {};
const int sequenceL[] = {};
const float beats[] = {};
const int bpm = 180 / 4;
#elif SONG == 3
/* Battle! (Wild Pokémon) (Black & White) - Composed by Junichi Masuda & Go Ichinose - Arranged by about@rorik.me */
//                       1                                                                                   2                                                                                   3                                 4                                    5                                 6                                   7                                 8                                     9                                   10                                11                          12                               13                                  14                                   15                              16                                  17                               18                                   19                              20                                       21                                22                                  23                                   24                              25                                 26                                      27                              28                                   29                                   30                                  31                                   32                              33                                  34                                      35                              36                                   37                                   38                                   39                                       40                          41                                      42                            43                              44                       45                                      46                           47                                   48                            49                                  50
const int sequenceR[] = {D4   , E4F  , E4   , E4F  , E4   , F4   , E4   , F4   , F4S  , F4   , F4S  , G4   , F4S  , G4   , G4S  , G4   , G4S  , A4   , G4S  , A4   , B4F  , A4   , B4F  , B4   , C5, RR, RR, G4, RR, RR , C5, RR , B4F, RR , RR , A4, RR, C5 , RR, RR , C4, SS, SS, SS, C5, SS , SS, SS , C4, SS , SS , C5, SS, SS , SS, SS , G4, RR, RR, C5, RR, RR , G4, RR , E5F, RR , RR , D5F, RR, C5 , SS, SS , E4F, SS, SS, SS, E5F, SS , SS, SS , G4, SS , SS, G5, SS, SS , SS, SS, C4, SS, F4, SS, SS, G4, SS, B4F, SS, SS, A4, SS, G4, F4, RR, E4F, SS, SS , A3, SS , SS, G4 , RR, E4F, G4, RR , B4F, SS , SS, SS , SS, A4, SS, SS, G4, SS, SS, F4, RR, B4F, SS, SS , A4, SS , SS, G4 , RR, E5F, SS, SS, SS, D5, SS, SS, SS, G4 , SS, SS , B4F, SS , SS, G4 , SS, A4, SS, SS, SS, SS, SS, SS, SS, C5, SS, SS, SS, SS, SS, G4, A4, B4F, C5, E5F, SS, SS, SS, F5 , SS, SS, SS, E5F, SS, SS , D5, SS , SS, B4F, SS, C5, SS, SS, SS, SS, SS, SS, E5F, E5, F5, SS, SS, SS, SS, SS, SS, SS, E5F, F5, RR , G5, SS , SS, SS, SS, B5F, SS, SS , A5, A5F, G5 , SS, SS, SS, F5, G5, RR, A5, SS, SS, F5, SS, C6, SS, SS, B5, B5F, A5, SS, SS, SS, G5 , A5, RR , B5F, SS , SS, G5 , SS, E6F, SS, SS , D5, SS , SS, B5F, SS, A5, SS, SS, SS, SS, SS, SS, B5F, B5, C6, SS, SS, SS, SS, SS, SS, SS, E4F, F4, RR , G4, SS , SS, SS , SS, B4F, SS, SS , A4, A4F, G4 , SS, SS, SS, F4, G4, RR, A4, SS, SS, F4, SS, C5, SS, SS, B4, B4F, A4, SS, SS, SS, G4 , A4, RR , B4F, SS , SS, E4F, SS, E5F, SS, D5 , SS , C5, SS, B4F, SS , C5  SS, SS, SS, SS, SS, SS, SS, E5F, E5, F5, SS, SS, SS, SS, SS, G5, A5F, SS , SS , SS , SS , SS , SS , SS , SS , SS , SS , SS , SS , G5 , F5, SS, SS, SS, SS, SS, SS, SS, SS, SS , SS, SS, SS, G5, A5F, SS , SS , SS , SS , SS , SS , SS , SS , SS, SS , SS , SS , A5 , B5F, SS , SS, SS , SS, SS , SS, SS , SS, SS, SS , SS, SS , SS, SS, SS, SS , SS, SS , SS, SS , SS, SS , SS, SS, SS , SS, SS , SS, SS};
const int sequenceL[] = {D2   , E2F  , E2   , E2F  , E2   , F2   , E2   , F2   , F2S  , F2   , F2S  , G2   , F2S  , G2   , G2S  , G2   , G2S  , A2   , G2S  , A2   , B2F  , A2   , B2F  , B2   , C2, C2, C2, C2, C2, G2F, F2, E2F, C2 , G2F, G2F, F2, SS, E2F, F2, E2F, C2, C2, C2, C2, C2, G2F, F2, E2F, C2, G2F, G2F, F2, SS, E2F, F2, E2F, C2, C2, C2, C2, C2, G2F, F2, E2F, C2 , G2F, G2F, F2 , SS, E2F, F2, E2F, C2 , C2, C2, C2, C2 , G2F, F2, E2F, C2, B2F, C2, F2, SS, E2F, F2, F2, C2, C2, G2, C2, G2, C2, G2, C2 , C2, C2, G2, C2, G2, C2, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2 , E2F, G2, E2F, G2, F2, A2, F2, A2, F2, A2, F2, A2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, C2 , G2, C3, G2, C2, C3, C2, G2, E2F, G2, E2F, G2 , E2F, G2, E2F, G2, F2, A2, F2, A2, F2, A2, F2, A2, F2, C2, F2, C2, F2, C2, F2, SS, C2 , SS, C2 , G2, C3, G2, B2F, C3, C2, F2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, F2, A2, F2, A2, F2, A2, F2, A2 , SS, F2, A2, F2, A2, F2, A2, F2, A2, E2F, G2, E2F, G2, E2F, G2, G2, G2, E2F, G2, E2F, G2, SS , E2F, G2, G2, G2, G2, F2, A2, F2, A2, F2, A2, F2, F2, A2, F2, A2, SS , F2, A2, F2, A2, E2F, G2, E2F, G2 , E2F, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, F2, A2, F2, A2, F2, A2, F2, A2 , SS, F2, C2, F2, C2, F2, C2, F2, C2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, E2F, G2, SS , E2F, G2, G2, G2, F2, A2, F2, A2, F2, A2, F2, A2, F2, A2, F2, A2, SS , F2, A2, F2, A2, E2F, G2, E2F, G2 , E2F, G2, E2F, G2, E2F, G2, E2F, B2F, G1, G1, G1 , E2F, F2, RR, F2, A2, C2, F2, A3, F2, A2 , SS, F2, C3, A2, A2, F2, F2, C2, E2F, A2F, E2F, A2F, E2F, A2F, E2F, A2F, E2F, B2F, A2F, E2F, A2F, E2F, C2, F2, C2, F2, C2, F2, C2, F2, C2, B2F, F2, C2, F2, C2, E2F, A2F, E2F, A2F, E2F, A2F, E2F, A2F, E2F, C3, B2F, A2F, E2F, A2F, F2 , B2F, F2, B2F, F2, B2F, F2, B2F, F2, F3, B2F, D3, B2F, D3, F3, F2, B2F, F2, B2F, F2, B2F, F2, B2F, F1, F2, B1F, D2, B1F, D2, F2};
const float beats[] =   {EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN TQ, EN, EN, EN, EN, EN, EN , EN, EN , EN , EN , EN , EN, EN, EN , EN, EN , EN, EN, EN, EN, EN, EN , EN, EN , EN, EN , EN , EN, EN, EN , EN, EN , EN, EN, EN, EN, EN, EN , EN, EN , EN , EN , EN , EN , EN, EN , EN, EN , EN , EN, EN, EN, EN , EN , EN, EN , EN, EN , EN, EN, EN, EN , EN, EN, QN, EN, EN, EN, EN, EN, EN, EN , EN, EN, EN, EN, EN, EN, EN, EN , EN, EN , EN, EN , EN, EN , EN, EN , EN, EN , EN , EN , EN, EN , EN, EN, EN, EN, EN, EN, EN, EN, EN, EN , EN, EN , EN, EN , EN, EN , EN, EN , EN, EN, EN, EN, EN, EN, EN, EN , EN, EN , EN , EN , EN, EN , EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, SN, SN, SN , SN, EN , EN, EN, EN, EN , EN, EN, EN, EN , EN, EN , EN, EN , EN, EN , EN, EN, EN, EN, EN, EN, EN, EN, SN , SN, EN, EN, EN, EN, EN, EN, EN, EN, EN , EN, EN , EN, EN , EN, EN, EN, EN , EN, EN , SN, SN , EN , EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, SN, SN , EN, EN, EN, EN, EN , EN, EN , EN , EN , EN, EN , EN, EN , EN, EN , EN, EN , EN, EN , EN, EN, EN, EN, EN, EN, EN, EN, SN , SN, SN, SN, SN, SN, SN, SN, SN, SN, EN , EN, EN , EN, EN , EN, EN , EN, EN , EN, EN , SN, SN , EN , EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, EN, SN, SN , EN, EN, EN, EN, EN , EN, EN , EN , EN , EN, EN , EN, EN , EN, EN , EN , EN, EN, EN , EN , SN, SN, EN, EN, EN, EN, EN, EN, SN , SN, EN, QN, EN, EN, EN, EN, EN, EN , EN , EN , EN , EN , EN , EN , EN , EN,  QN , QN , EN , EN , EN , EN, EN, EN, EN, EN, EN, EN, EN, EN, QN , QN, EN, EN, EN, EN , EN , EN , EN , EN , EN , EN , EN , EN , QN, QN , EN , EN , EN , EN , EN , EN, EN , EN, EN , EN, EN , EN, EN, EN , QN, EN , EN, EN, EN, EN , EN, EN , EN, EN , EN, EN , EN, EN, EN , QN, EN , EN, EN};
const int bpm = 180 / 4;
#elif SONG == 4
/* Battle! (Trainer Battle) (Red & Blue) - Composed by Junichi Masuda - Arranged by about@rorik.me */
const int sequenceR[] = {};
const int sequenceL[] = {};
const float beats[] = {};
const int bpm = 180 / 4;
#elif SONG == 5
/* Battle! (Trainer Battle) (Ruby & Shapphire) - Composed by Junichi Masuda - Arranged by about@rorik.me */
const int sequenceR[] = {};
const int sequenceL[] = {};
const float beats[] = {};
const int bpm = 180 / 4;
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
