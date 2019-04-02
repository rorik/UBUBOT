#pragma region Tones

#define B8 7902
#define B8F 7459
#define A8S 7459
#define A8 7040
#define A8F 6645
#define G8S 6645
#define G8 6272
#define G8F 5920
#define F8S 5920
#define F8 5588
#define E8 5274
#define E8F 4978
#define D8S 4978
#define D8 4699
#define D8F 4435
#define C8S 4435
#define C8 4186

#define B7 3951
#define B7F 3729
#define A7S 3729
#define A7 3520
#define A7F 3322
#define G7S 3322
#define G7 3136
#define G7F 2960
#define F7S 2960
#define F7 2794
#define E7 2637
#define E7F 2489
#define D7S 2489
#define D7 2349
#define D7F 2217
#define C7S 2217
#define C7 2093

#define B6 1976
#define B6F 1865
#define A6S 1865
#define A6 1760
#define A6F 1661
#define G6S 1661
#define G6 1568
#define G6F 1480
#define F6S 1480
#define F6 1397
#define E6 1319
#define E6F 1245
#define D6S 1245
#define D6 1175
#define D6F 1109
#define C6S 1109
#define C6 1047

#define B5 988
#define B5F 932
#define A5S 932
#define A5 880
#define A5F 831
#define G5S 831
#define G5 784
#define G5F 740
#define F5S 740
#define F5 698
#define E5 659
#define E5F 622
#define D5S 622
#define D5 587
#define D5F 554
#define C5S 554
#define C5 523

#define B4 494
#define B4F 466
#define A4S 466
#define A4 440
#define A4F 415
#define G4S 415
#define G4 392
#define G4F 370
#define F4S 370
#define F4 349
#define E4 330
#define E4F 311
#define D4S 311
#define D4 294
#define D4F 277
#define C4S 277
#define C4 262

#define B3 247
#define B3F 233
#define A3S 233
#define A3 220
#define A3F 208
#define G3S 208
#define G3 196
#define G3F 185
#define F3S 185
#define F3 175
#define E3 165
#define E3F 156
#define D3S 156
#define D3 147
#define D3F 139
#define C3S 139
#define C3 131

#define B2 123
#define B2F 117
#define A2S 117
#define A2 110
#define A2F 104
#define G2S 104
#define G2 98
#define G2F 92
#define F2S 92
#define F2 87
#define E2 82
#define E2F 78
#define D2S 78
#define D2 73
#define D2F 69
#define C2S 69
#define C2 65

#define B1 62
#define B1F 58
#define A1S 58
#define A1 55
#define A1F 52
#define G1S 52
#define G1 49
#define G1F 46
#define F1S 46
#define F1 44
#define E1 41
#define E1F 39
#define D1S 39
#define D1 37
#define D1F 35
#define C1S 35
#define C1 33

#define B0 31
#define B0F 29
#define A0S 29
#define A0 28
#define A0F 26
#define G0S 26
#define G0 25
#define G0F 23
#define F0S 23
#define F0 22
#define E0 21
#define E0F 19
#define D0S 19
#define D0 18
#define D0F 17
#define C0S 17
#define C0 16

#pragma endregion


#pragma region Special notes

// Rest
#define RR 0
// Sustain previous note
#define SS -1

#pragma endregion


#pragma region Durations

// Octuple whole note / Maxima / Large
#define DL 8
// Quadruple whole note / Long
#define LG 4
// Double whole note / Breve
#define DN 2
// Whole note / Semibreve
#define WN 1
// Half note / Minim
#define HN 0.5
// Quarter note / Crotchet
#define QN 0.25
// Eighth note / Quaver
#define EN 0.125
// Sixteenth note / Semiquaver
#define SN 0.0625
// Thiry-second note / Demisemiquaver
#define TN 0.03125

#pragma endregion


#pragma region Duration accidentals

// Dot
#define DT * 1.5
// Double dot
#define DTT * 1.75
// Triple dot
#define DTTT * 1.875

// Tuplets
// Three quarters
#define TQ * 0.75
// Five quarters
#define FQ * 1.25

#pragma endregion