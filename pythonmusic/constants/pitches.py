__all__ = [
    "REST",
    "C_1",
    "CS_1",
    "DF_1",
    "D_1",
    "DS_1",
    "EF_1",
    "E_1",
    "ES_1",
    "FF_1",
    "F_1",
    "FS_1",
    "GF_1",
    "G_1",
    "GS_1",
    "AF_1",
    "A_1",
    "AS_1",
    "BF_1",
    "B_1",
    "BS_1",
    "CF0",
    "C0",
    "CS0",
    "DF0",
    "D0",
    "DS0",
    "EF0",
    "E0",
    "ES0",
    "FF0",
    "F0",
    "FS0",
    "GF0",
    "G0",
    "GS0",
    "AF0",
    "A0",
    "AS0",
    "BF0",
    "B0",
    "BS0",
    "CF1",
    "C1",
    "CS1",
    "DF1",
    "D1",
    "DS1",
    "EF1",
    "E1",
    "ES1",
    "FF1",
    "F1",
    "FS1",
    "GF1",
    "G1",
    "GS1",
    "AF1",
    "A1",
    "AS1",
    "BF1",
    "B1",
    "BS1",
    "CF2",
    "C2",
    "CS2",
    "DF2",
    "D2",
    "DS2",
    "EF2",
    "E2",
    "ES2",
    "FF2",
    "F2",
    "FS2",
    "GF2",
    "G2",
    "GS2",
    "AF2",
    "A2",
    "AS2",
    "BF2",
    "B2",
    "BS2",
    "CF3",
    "C3",
    "CS3",
    "DF3",
    "D3",
    "DS3",
    "EF3",
    "E3",
    "ES3",
    "FF3",
    "F3",
    "FS3",
    "GF3",
    "G3",
    "GS3",
    "AF3",
    "A3",
    "AS3",
    "BF3",
    "B3",
    "BS3",
    "CF4",
    "C4",
    "CS4",
    "DF4",
    "D4",
    "DS4",
    "EF4",
    "E4",
    "ES4",
    "FF4",
    "F4",
    "FS4",
    "GF4",
    "G4",
    "GS4",
    "AF4",
    "A4",
    "AS4",
    "BF4",
    "B4",
    "BS4",
    "CF5",
    "C5",
    "CS5",
    "DF5",
    "D5",
    "DS5",
    "EF5",
    "E5",
    "ES5",
    "FF5",
    "F5",
    "FS5",
    "GF5",
    "G5",
    "GS5",
    "AF5",
    "A5",
    "AS5",
    "BF5",
    "B5",
    "BS5",
    "CF6",
    "C6",
    "CS6",
    "DF6",
    "D6",
    "DS6",
    "EF6",
    "E6",
    "ES6",
    "FF6",
    "F6",
    "FS6",
    "GF6",
    "G6",
    "GS6",
    "AF6",
    "A6",
    "AS6",
    "BF6",
    "B6",
    "BS6",
    "CF7",
    "C7",
    "CS7",
    "DF7",
    "D7",
    "DS7",
    "EF7",
    "E7",
    "ES7",
    "FF7",
    "F7",
    "FS7",
    "GF7",
    "G7",
    "GS7",
    "AF7",
    "A7",
    "AS7",
    "BF7",
    "B7",
    "BS7",
    "CF8",
    "C8",
    "CS8",
    "DF8",
    "D8",
    "DS8",
    "EF8",
    "E8",
    "ES8",
    "FF8",
    "F8",
    "FS8",
    "GF8",
    "G8",
    "GS8",
    "AF8",
    "A8",
    "AS8",
    "BF8",
    "B8",
    "BS8",
    "CF9",
    "C9",
    "CS9",
    "DF9",
    "D9",
    "DS9",
    "EF9",
    "E9",
    "ES9",
    "FF9",
    "F9",
    "FS9",
    "GF9",
    "G9",
]

REST: int = -1
"""
Rest pitch constant.

This value does not correspont to a valid MIDI value. Rests are handled
internally during conversion.

.. important:: Sending this value to a midi device could result in undefined
    behaviour.
"""

C_1: int = 0
"""Pitch constant for C_1, MIDI pitch 0"""

CS_1: int = 1
"""Pitch constant for C#/Db_1, MIDI pitch 1"""

DF_1: int = 1
"""Pitch constant for Db/C#_1, MIDI pitch 1"""

D_1: int = 2
"""Pitch constant for D_1, MIDI pitch 2"""

DS_1: int = 3
"""Pitch constant for D#/Eb_1, MIDI pitch 3"""

EF_1: int = 3
"""Pitch constant for Eb/D#_1, MIDI pitch 3"""

E_1: int = 4
"""Pitch constant for E_1, MIDI pitch 4"""

ES_1: int = 5
"""Pitch constant for E#/F_1, MIDI pitch 5"""

FF_1: int = 4
"""Pitch constant for Fb/E_1, MIDI pitch 4"""

F_1: int = 5
"""Pitch constant for F_1, MIDI pitch 5"""

FS_1: int = 6
"""Pitch constant for F#/Gb_1, MIDI pitch 6"""

GF_1: int = 6
"""Pitch constant for Gb/F#_1, MIDI pitch 6"""

G_1: int = 7
"""Pitch constant for G_1, MIDI pitch 7"""

GS_1: int = 8
"""Pitch constant for G#/Ab_1, MIDI pitch 8"""

AF_1: int = 8
"""Pitch constant for Ab/G#_1, MIDI pitch 8"""

A_1: int = 9
"""Pitch constant for A_1, MIDI pitch 9"""

AS_1: int = 10
"""Pitch constant for A#/Bb_1, MIDI pitch 10"""

BF_1: int = 10
"""Pitch constant for Bb/A#_1, MIDI pitch 10"""

B_1: int = 11
"""Pitch constant for B_1, MIDI pitch 11"""

BS_1: int = 12
"""Pitch constant for B#/C0, MIDI pitch 12"""

CF0: int = 11
"""Pitch constant for Cb_0/B_1, MIDI pitch 11"""

C0: int = 12
"""Pitch constant for C0, MIDI pitch 12"""

CS0: int = 13
"""Pitch constant for C#/Db0, MIDI pitch 13"""

DF0: int = 13
"""Pitch constant for Db/C#0, MIDI pitch 13"""

D0: int = 14
"""Pitch constant for D0, MIDI pitch 14"""

DS0: int = 15
"""Pitch constant for D#/Eb0, MIDI pitch 15"""

EF0: int = 15
"""Pitch constant for Eb/D#0, MIDI pitch 15"""

E0: int = 16
"""Pitch constant for E0, MIDI pitch 16"""

ES0: int = 17
"""Pitch constant for E#/F0, MIDI pitch 17"""

FF0: int = 16
"""Pitch constant for Fb/E0, MIDI pitch 16"""

F0: int = 17
"""Pitch constant for F0, MIDI pitch 17"""

FS0: int = 18
"""Pitch constant for F#/Gb0, MIDI pitch 18"""

GF0: int = 18
"""Pitch constant for Gb/F#0, MIDI pitch 18"""

G0: int = 19
"""Pitch constant for G0, MIDI pitch 19"""

GS0: int = 20
"""Pitch constant for G#/Ab0, MIDI pitch 20"""

AF0: int = 20
"""Pitch constant for Ab/G#0, MIDI pitch 20"""

A0: int = 21
"""Pitch constant for A0, MIDI pitch 21"""

AS0: int = 22
"""Pitch constant for A#/Bb0, MIDI pitch 22"""

BF0: int = 22
"""Pitch constant for Bb/A#0, MIDI pitch 22"""

B0: int = 23
"""Pitch constant for B0, MIDI pitch 23"""

BS0: int = 24
"""Pitch constant for B#/C1, MIDI pitch 24"""

CF1: int = 23
"""Pitch constant for Cb1/B0, MIDI pitch 23"""

C1: int = 24
"""Pitch constant for C1, MIDI pitch 24"""

CS1: int = 25
"""Pitch constant for C#/Db1, MIDI pitch 25"""

DF1: int = 25
"""Pitch constant for Db/C#1, MIDI pitch 25"""

D1: int = 26
"""Pitch constant for D1, MIDI pitch 26"""

DS1: int = 27
"""Pitch constant for D#/Eb1, MIDI pitch 27"""

EF1: int = 27
"""Pitch constant for Eb/D#1, MIDI pitch 27"""

E1: int = 28
"""Pitch constant for E1, MIDI pitch 28"""

ES1: int = 29
"""Pitch constant for E#/F1, MIDI pitch 29"""

FF1: int = 28
"""Pitch constant for Fb/E1, MIDI pitch 28"""

F1: int = 29
"""Pitch constant for F1, MIDI pitch 29"""

FS1: int = 30
"""Pitch constant for F#/Gb1, MIDI pitch 30"""

GF1: int = 30
"""Pitch constant for Gb/F#1, MIDI pitch 30"""

G1: int = 31
"""Pitch constant for G1, MIDI pitch 31"""

GS1: int = 32
"""Pitch constant for G#/Ab1, MIDI pitch 32"""

AF1: int = 32
"""Pitch constant for Ab/G#1, MIDI pitch 32"""

A1: int = 33
"""Pitch constant for A1, MIDI pitch 33"""

AS1: int = 34
"""Pitch constant for A#/Bb1, MIDI pitch 34"""

BF1: int = 34
"""Pitch constant for Bb/A#1, MIDI pitch 34"""

B1: int = 35
"""Pitch constant for B1, MIDI pitch 35"""

BS1: int = 36
"""Pitch constant for B#/C2, MIDI pitch 36"""

CF2: int = 35
"""Pitch constant for Cb2/B1, MIDI pitch 35"""

C2: int = 36
"""Pitch constant for C2, MIDI pitch 36"""

CS2: int = 37
"""Pitch constant for C#/Db2, MIDI pitch 37"""

DF2: int = 37
"""Pitch constant for Db/C#2, MIDI pitch 37"""

D2: int = 38
"""Pitch constant for D2, MIDI pitch 38"""

DS2: int = 39
"""Pitch constant for D#/Eb2, MIDI pitch 39"""

EF2: int = 39
"""Pitch constant for Eb/D#2, MIDI pitch 39"""

E2: int = 40
"""Pitch constant for E2, MIDI pitch 40"""

ES2: int = 41
"""Pitch constant for E#/F2, MIDI pitch 41"""

FF2: int = 40
"""Pitch constant for Fb/E2, MIDI pitch 40"""

F2: int = 41
"""Pitch constant for F2, MIDI pitch 41"""

FS2: int = 42
"""Pitch constant for F#/Gb2, MIDI pitch 42"""

GF2: int = 42
"""Pitch constant for Gb/F#2, MIDI pitch 42"""

G2: int = 43
"""Pitch constant for G2, MIDI pitch 43"""

GS2: int = 44
"""Pitch constant for G#/Ab2, MIDI pitch 44"""

AF2: int = 44
"""Pitch constant for Ab/G#2, MIDI pitch 44"""

A2: int = 45
"""Pitch constant for A2, MIDI pitch 45"""

AS2: int = 46
"""Pitch constant for A#/Bb2, MIDI pitch 46"""

BF2: int = 46
"""Pitch constant for Bb/A#2, MIDI pitch 46"""

B2: int = 47
"""Pitch constant for B2, MIDI pitch 47"""

BS2: int = 48
"""Pitch constant for B#/C3, MIDI pitch 48"""

CF3: int = 47
"""Pitch constant for Cb3/B2, MIDI pitch 47"""

C3: int = 48
"""Pitch constant for C3, MIDI pitch 48"""

CS3: int = 49
"""Pitch constant for C#/Db3, MIDI pitch 49"""

DF3: int = 49
"""Pitch constant for Db/C#3, MIDI pitch 49"""

D3: int = 50
"""Pitch constant for D3, MIDI pitch 50"""

DS3: int = 51
"""Pitch constant for D#/Eb3, MIDI pitch 51"""

EF3: int = 51
"""Pitch constant for Eb/D#3, MIDI pitch 51"""

E3: int = 52
"""Pitch constant for E3, MIDI pitch 52"""

ES3: int = 53
"""Pitch constant for E#/F3, MIDI pitch 53"""

FF3: int = 52
"""Pitch constant for Fb/E3, MIDI pitch 52"""

F3: int = 53
"""Pitch constant for F3, MIDI pitch 53"""

FS3: int = 54
"""Pitch constant for F#/Gb3, MIDI pitch 54"""

GF3: int = 54
"""Pitch constant for Gb/F#3, MIDI pitch 54"""

G3: int = 55
"""Pitch constant for G3, MIDI pitch 55"""

GS3: int = 56
"""Pitch constant for G#/Ab3, MIDI pitch 56"""

AF3: int = 56
"""Pitch constant for Ab/G#3, MIDI pitch 56"""

A3: int = 57
"""Pitch constant for A3, MIDI pitch 57"""

AS3: int = 58
"""Pitch constant for A#/Bb3, MIDI pitch 58"""

BF3: int = 58
"""Pitch constant for Bb/A#3, MIDI pitch 58"""

B3: int = 59
"""Pitch constant for B3, MIDI pitch 59"""

BS3: int = 60
"""Pitch constant for B#/C4, MIDI pitch 60"""

CF4: int = 59
"""Pitch constant for Cb4/B3, MIDI pitch 59"""

C4: int = 60
"""Pitch constant for C4, MIDI pitch 60"""

CS4: int = 61
"""Pitch constant for C#/Db4, MIDI pitch 61"""

DF4: int = 61
"""Pitch constant for Db/C#4, MIDI pitch 61"""

D4: int = 62
"""Pitch constant for D4, MIDI pitch 62"""

DS4: int = 63
"""Pitch constant for D#/Eb4, MIDI pitch 63"""

EF4: int = 63
"""Pitch constant for Eb/D#4, MIDI pitch 63"""

E4: int = 64
"""Pitch constant for E4, MIDI pitch 64"""

ES4: int = 65
"""Pitch constant for E#/F4, MIDI pitch 65"""

FF4: int = 64
"""Pitch constant for Fb/E4, MIDI pitch 64"""

F4: int = 65
"""Pitch constant for F4, MIDI pitch 65"""

FS4: int = 66
"""Pitch constant for F#/Gb4, MIDI pitch 66"""

GF4: int = 66
"""Pitch constant for Gb/F#4, MIDI pitch 66"""

G4: int = 67
"""Pitch constant for G4, MIDI pitch 67"""

GS4: int = 68
"""Pitch constant for G#/Ab4, MIDI pitch 68"""

AF4: int = 68
"""Pitch constant for Ab/G#4, MIDI pitch 68"""

A4: int = 69
"""Pitch constant for A4, MIDI pitch 69"""

AS4: int = 70
"""Pitch constant for A#/Bb4, MIDI pitch 70"""

BF4: int = 70
"""Pitch constant for Bb/A#4, MIDI pitch 70"""

B4: int = 71
"""Pitch constant for B4, MIDI pitch 71"""

BS4: int = 72
"""Pitch constant for B#/C5, MIDI pitch 72"""

CF5: int = 71
"""Pitch constant for Cb5/B4, MIDI pitch 71"""

C5: int = 72
"""Pitch constant for C5, MIDI pitch 72"""

CS5: int = 73
"""Pitch constant for C#/Db5, MIDI pitch 73"""

DF5: int = 73
"""Pitch constant for Db/C#5, MIDI pitch 73"""

D5: int = 74
"""Pitch constant for D5, MIDI pitch 74"""

DS5: int = 75
"""Pitch constant for D#/Eb5, MIDI pitch 75"""

EF5: int = 75
"""Pitch constant for Eb/D#5, MIDI pitch 75"""

E5: int = 76
"""Pitch constant for E5, MIDI pitch 76"""

ES5: int = 77
"""Pitch constant for E#/F5, MIDI pitch 77"""

FF5: int = 76
"""Pitch constant for Fb/E5, MIDI pitch 76"""

F5: int = 77
"""Pitch constant for F5, MIDI pitch 77"""

FS5: int = 78
"""Pitch constant for F#/Gb5, MIDI pitch 78"""

GF5: int = 78
"""Pitch constant for Gb/F#5, MIDI pitch 78"""

G5: int = 79
"""Pitch constant for G5, MIDI pitch 79"""

GS5: int = 80
"""Pitch constant for G#/Ab5, MIDI pitch 80"""

AF5: int = 80
"""Pitch constant for Ab/G#5, MIDI pitch 80"""

A5: int = 81
"""Pitch constant for A5, MIDI pitch 81"""

AS5: int = 82
"""Pitch constant for A#/Bb5, MIDI pitch 82"""

BF5: int = 82
"""Pitch constant for Bb/A#5, MIDI pitch 82"""

B5: int = 83
"""Pitch constant for B5, MIDI pitch 83"""

BS5: int = 84
"""Pitch constant for B#/C6, MIDI pitch 84"""

CF6: int = 83
"""Pitch constant for Cb6/B5, MIDI pitch 83"""

C6: int = 84
"""Pitch constant for C6, MIDI pitch 84"""

CS6: int = 85
"""Pitch constant for C#/Db6, MIDI pitch 85"""

DF6: int = 85
"""Pitch constant for Db/C#6, MIDI pitch 85"""

D6: int = 86
"""Pitch constant for D6, MIDI pitch 86"""

DS6: int = 87
"""Pitch constant for D#/Eb6, MIDI pitch 87"""

EF6: int = 87
"""Pitch constant for Eb/D#6, MIDI pitch 87"""

E6: int = 88
"""Pitch constant for E6, MIDI pitch 88"""

ES6: int = 89
"""Pitch constant for E#/F6, MIDI pitch 89"""

FF6: int = 88
"""Pitch constant for Fb/E6, MIDI pitch 88"""

F6: int = 89
"""Pitch constant for F6, MIDI pitch 89"""

FS6: int = 90
"""Pitch constant for F#/Gb6, MIDI pitch 90"""

GF6: int = 90
"""Pitch constant for Gb/F#6, MIDI pitch 90"""

G6: int = 91
"""Pitch constant for G6, MIDI pitch 91"""

GS6: int = 92
"""Pitch constant for G#/Ab6, MIDI pitch 92"""

AF6: int = 92
"""Pitch constant for Ab/G#6, MIDI pitch 92"""

A6: int = 93
"""Pitch constant for A6, MIDI pitch 93"""

AS6: int = 94
"""Pitch constant for A#/Bb6, MIDI pitch 94"""

BF6: int = 94
"""Pitch constant for Bb/A#6, MIDI pitch 94"""

B6: int = 95
"""Pitch constant for B6, MIDI pitch 95"""

BS6: int = 96
"""Pitch constant for B#/C7, MIDI pitch 96"""

CF7: int = 95
"""Pitch constant for Cb7/B6, MIDI pitch 95"""

C7: int = 96
"""Pitch constant for C7, MIDI pitch 96"""

CS7: int = 97
"""Pitch constant for C#/Db7, MIDI pitch 97"""

DF7: int = 97
"""Pitch constant for Db/C#7, MIDI pitch 97"""

D7: int = 98
"""Pitch constant for D7, MIDI pitch 98"""

DS7: int = 99
"""Pitch constant for D#/Eb7, MIDI pitch 99"""

EF7: int = 99
"""Pitch constant for Eb/D#7, MIDI pitch 99"""

E7: int = 100
"""Pitch constant for E7, MIDI pitch 100"""

ES7: int = 101
"""Pitch constant for E#/F7, MIDI pitch 101"""

FF7: int = 100
"""Pitch constant for Fb/E7, MIDI pitch 100"""

F7: int = 101
"""Pitch constant for F7, MIDI pitch 101"""

FS7: int = 102
"""Pitch constant for F#/Gb7, MIDI pitch 102"""

GF7: int = 102
"""Pitch constant for Gb/F#7, MIDI pitch 102"""

G7: int = 103
"""Pitch constant for G7, MIDI pitch 103"""

GS7: int = 104
"""Pitch constant for G#/Ab7, MIDI pitch 104"""

AF7: int = 104
"""Pitch constant for Ab/G#7, MIDI pitch 104"""

A7: int = 105
"""Pitch constant for A7, MIDI pitch 105"""

AS7: int = 106
"""Pitch constant for A#/Bb7, MIDI pitch 106"""

BF7: int = 106
"""Pitch constant for Bb/A#7, MIDI pitch 106"""

B7: int = 107
"""Pitch constant for B7, MIDI pitch 107"""

BS7: int = 108
"""Pitch constant for B#/C8, MIDI pitch 108"""

CF8: int = 107
"""Pitch constant for Cb8/B7, MIDI pitch 107"""

C8: int = 108
"""Pitch constant for C8, MIDI pitch 108"""

CS8: int = 109
"""Pitch constant for C#/Db8, MIDI pitch 109"""

DF8: int = 109
"""Pitch constant for Db/C#8, MIDI pitch 109"""

D8: int = 110
"""Pitch constant for D8, MIDI pitch 110"""

DS8: int = 111
"""Pitch constant for D#/Eb8, MIDI pitch 111"""

EF8: int = 111
"""Pitch constant for Eb/D#8, MIDI pitch 111"""

E8: int = 112
"""Pitch constant for E8, MIDI pitch 112"""

ES8: int = 113
"""Pitch constant for E#/F8, MIDI pitch 113"""

FF8: int = 112
"""Pitch constant for Fb/E8, MIDI pitch 112"""

F8: int = 113
"""Pitch constant for F8, MIDI pitch 113"""

FS8: int = 114
"""Pitch constant for F#/Gb8, MIDI pitch 114"""

GF8: int = 114
"""Pitch constant for Gb/F#8, MIDI pitch 114"""

G8: int = 115
"""Pitch constant for G8, MIDI pitch 115"""

GS8: int = 116
"""Pitch constant for G#/Ab8, MIDI pitch 116"""

AF8: int = 116
"""Pitch constant for Ab/G#8, MIDI pitch 116"""

A8: int = 117
"""Pitch constant for A8, MIDI pitch 117"""

AS8: int = 118
"""Pitch constant for A#/Bb8, MIDI pitch 118"""

BF8: int = 118
"""Pitch constant for Bb/A#8, MIDI pitch 118"""

B8: int = 119
"""Pitch constant for B8, MIDI pitch 119"""

BS8: int = 120
"""Pitch constant for B#/C9, MIDI pitch 120"""

CF9: int = 119
"""Pitch constant for Cb9/B8, MIDI pitch 119"""

C9: int = 120
"""Pitch constant for C9, MIDI pitch 120"""

CS9: int = 121
"""Pitch constant for C#/Db9, MIDI pitch 121"""

DF9: int = 121
"""Pitch constant for Db/C#9, MIDI pitch 121"""

D9: int = 122
"""Pitch constant for D9, MIDI pitch 122"""

DS9: int = 123
"""Pitch constant for D#/Eb9, MIDI pitch 123"""

EF9: int = 123
"""Pitch constant for Eb/D#9, MIDI pitch 123"""

E9: int = 124
"""Pitch constant for E9, MIDI pitch 124"""

ES9: int = 125
"""Pitch constant for E#/F9, MIDI pitch 125"""

FF9: int = 124
"""Pitch constant for Fb/E9, MIDI pitch 124"""

F9: int = 125
"""Pitch constant for F9, MIDI pitch 125"""

FS9: int = 126
"""Pitch constant for F#/Gb9, MIDI pitch 126"""

GF9: int = 126
"""Pitch constant for Gb/F#9, MIDI pitch 126"""

G9: int = 127
"""Pitch constant for G9, MIDI pitch 127"""
