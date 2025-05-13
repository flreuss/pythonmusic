"""
O Fortuna
Carmina Burana
Carl Orff
"""

from time import sleep

from pythonmusic import *

BREATH = HN


def flute_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_notes_by_lists([E6, F6, D6, D6], [WN, HN], [MF])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_notes_by_lists(
        [A6, G6, A6, G6, G6, F6, E6], [WN, HN, HN, HN, HN, HN, WWN + WN], [MF]
    )
    phrase_b.add_rest(BREATH)

    return Part("Flutes", FLUTE, [phrase_a, phrase_a, phrase_b])


def oboe_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([D5, F5, A5], [WN], [MF])
    phrase_a.add_chord_by_lists([C5, E5, A5], [HN], [MF])
    phrase_a.add_chord_by_lists([C5, D5, A5], [HN], [MF])
    phrase_a.add_chord_by_lists([BF4, D5, A5], [HN], [MF])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([F5, A5, E6], [WN], [MF])
    phrase_b.add_chord_by_lists([E5, G5, F6], [HN], [MF])
    phrase_b.add_chord_by_lists([F5, A5, E6], [HN], [MF])
    phrase_b.add_chord_by_lists([E5, G5, F6], [HN], [MF])
    phrase_b.add_chord_by_lists([E5, G5, F6], [HN], [MF])
    phrase_b.add_chord_by_lists([F5, A5, E6], [HN], [MF])
    phrase_b.add_chord_by_lists([E5, A5, E6], [WWN + WN], [MF])
    phrase_b.add_rest(BREATH)

    return Part("Oboes&English Horn", OBOE, [phrase_a, phrase_a, phrase_b])


def clarinet_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([F5, A5, E6], [WN], [MF])
    phrase_a.add_chord_by_lists([E5, A5, F6], [HN], [MF])
    phrase_a.add_chord_by_lists([D5, A5, D6], [HN], [MF])
    phrase_a.add_chord_by_lists([D5, A5, D6], [HN], [MF])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([F5, A5, E6], [WN], [MF])
    phrase_b.add_chord_by_lists([E5, G5, D6], [HN], [MF])
    phrase_b.add_chord_by_lists([F5, A5, E6], [HN], [MF])
    phrase_b.add_chord_by_lists([E5, G5, D6], [HN], [MF])
    phrase_b.add_chord_by_lists([E5, G5, D6], [HN], [MF])
    phrase_b.add_chord_by_lists([F5, A5, E6], [HN], [MF])
    phrase_b.add_chord_by_lists([E5, A5, E6], [WWN + WN], [MF])
    phrase_b.add_rest(BREATH)

    return Part("Clarinet", CLARINET, [phrase_a, phrase_a, phrase_b])


def bassoon_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_notes(
        [Note(D3, WN, MF), Note(C3, WN, MF), Note(BF2, WN, MF), Note.rest(BREATH)]
    )

    phrase_b = Phrase()
    phrase_b.add_notes(
        [Note(A2, WN, MP), Note(A3, WWN + WN + WWN + WN, MP), Note.rest(BREATH)]
    )

    return Part("Bassoon", BASSOON, [phrase_a, phrase_a, phrase_b])


def horn_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([A2, E3, A4, E5], [WN], [MP])
    phrase_a.add_chord_by_lists([A2, E3, A4, E5], [HN], [MP])
    phrase_a.add_chord_by_lists([A2, E3, A4, E5], [HN], [MP])
    phrase_a.add_chord_by_lists([A2, E3, A4, E5], [HN], [MP])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([E3, E5], [WN], [MP])
    phrase_b.add_chord_by_lists([E3, E5], [HN], [MP])
    phrase_b.add_chord_by_lists([E3, E5], [HN], [MP])
    phrase_b.add_chord_by_lists([E3, E5], [HN], [MP])
    phrase_b.add_chord_by_lists([E3, E5], [HN], [MP])
    phrase_b.add_chord_by_lists([E3, E5], [HN], [MP])
    phrase_b.add_chord_by_lists([E3, E5], [WWN + WN], [MP])
    phrase_b.add_rest(BREATH)

    return Part("Horns", FRENCH_HORNS, [phrase_a, phrase_a, phrase_b])


def trumpet_part() -> Part:
    # trumpets are often notated in a different key
    # this will be corrected later
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([G4, E5, FS5], [WN], [MP])
    phrase_a.add_chord_by_lists([FS4, D5, G5], [HN], [MP])
    phrase_a.add_chord_by_lists([E4, D5, E5], [HN], [MP])
    phrase_a.add_chord_by_lists([E4, C4, E5], [HN], [MP])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([FS5, G5, B5], [WN], [MP])
    phrase_b.add_chord_by_lists([E5, FS5, A5], [HN], [MP])
    phrase_b.add_chord_by_lists([FS5, G5, B5], [HN], [MP])
    phrase_b.add_chord_by_lists([E5, FS5, A5], [HN], [MP])
    phrase_b.add_chord_by_lists([E5, FS5, A5], [HN], [MP])
    phrase_b.add_chord_by_lists([E5, FS5, G5], [HN], [MP])
    phrase_b.add_chord_by_lists([G4, FS5], [WWN + WN], [MP])
    phrase_b.add_rest(BREATH)

    # correct for pitch
    phrase_a = mods.pitch_phrase(phrase_a, -MAJOR_SECOND)
    phrase_b = mods.pitch_phrase(phrase_b, -MAJOR_SECOND)

    return Part("Trumpets", TRUMPET, [phrase_a, phrase_a, phrase_b])


def trombone_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([F3, D4, E4], [WN], [MP])
    phrase_a.add_chord_by_lists([E3, C4, F4], [HN], [MP])
    phrase_a.add_chord_by_lists([D3, C4, D4], [HN], [MP])
    phrase_a.add_chord_by_lists([D3, BF3, D4], [HN], [MP])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([E4, F4, A4], [WN], [MP])
    phrase_b.add_chord_by_lists([D4, E4, G4], [HN], [MP])
    phrase_b.add_chord_by_lists([E4, F4, A4], [HN], [MP])
    phrase_b.add_chord_by_lists([D4, E4, G4], [HN], [MP])
    phrase_b.add_chord_by_lists([D4, E4, G4], [HN], [MP])
    phrase_b.add_chord_by_lists([E4, D4, F4], [HN], [MP])
    phrase_b.add_chord_by_lists([A3, E4, E4], [WWN + WN], [MP])
    phrase_b.add_rest(BREATH)

    return Part("Trombones", TROMBONE, [phrase_a, phrase_a, phrase_b])


def tuba_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_notes(
        [Note(D2, WN, MP), Note(C2, WN, MP), Note(BF2, WN, MP), Note.rest(BREATH)]
    )

    phrase_b = Phrase()
    phrase_b.add_notes(
        [Note(A2, WN, MP), Note(A3, WWN + WN + WWN + WN, MP), Note.rest(BREATH)]
    )

    return Part("Tuba", TUBA, [phrase_a, phrase_a, phrase_b])


def timpani_part() -> Part:
    phrase = Phrase()

    phrase.add_notes([Note(D3, HN, MF).with_accent()] * 6)
    phrase.add_rest(BREATH)
    phrase.add_notes([Note(D3, HN, MF).with_accent()] * 6)
    phrase.add_rest(BREATH)

    phrase.add_note(Note(A2, WN, MF).with_accent())
    # trill
    phrase.add_notes(
        [Note(A2, SN, FF, [PORTATO])] * round(((WWN + WN + WWN + WN - QN) / SN))
    )
    phrase.add_note(Note(A2, QN, MF))

    part = Part("Timpani", TIMPANI, [phrase])
    return part


def choir_part() -> Part:
    phrase = Phrase()
    phrase.add_rest(HN)
    phrase.add_chord_by_lists([F3, D4, E4, F4, D5, E5], [WN], [MF])
    phrase.add_chord_by_lists([E3, C4, F4, E4, C5, F5], [HN], [MF])
    phrase.add_chord_by_lists([D3, C4, D4, D4, C5, D5], [HN], [MF])
    phrase.add_chord_by_lists([D3, BF3, D4, D4, BF4, D5], [HN], [MF])
    phrase.add_rest(BREATH)
    phrase = mods.repeat_phrase(phrase, 2)

    phrase.add_rest(HN)
    phrase.add_chord_by_lists([A3, E5, A4, F5, A5], [WN], [MF])
    phrase.add_chord_by_lists([A3, A4, E4, G4, E5, G5], [HN], [MF])
    phrase.add_chord_by_lists([A3, A4, F4, A4, F5, A5], [HN], [MF])
    phrase.add_chord_by_lists([A3, A4, E4, G4, E5, G5], [HN], [MF])
    phrase.add_chord_by_lists([A3, A4, E4, G4, E5, G5], [HN], [MF])
    phrase.add_chord_by_lists([A3, A4, D4, F4, D5, F5], [HN], [MF])
    phrase.add_chord_by_lists([A3, A4, E4, E5], [WWN + WN], [MF])
    phrase.add_rest(BREATH)

    part = Part("Choir", CHOIR_AAHS, [phrase])
    return part


def piano_part() -> Part:
    rpa: list[Chord] = [
        Chord.from_lists([F4, A4, E5], [WN], [MF]),
        Chord.from_lists([E4, A4, F5], [HN], [MF]),
        Chord.from_lists([D3, C4, D4], [HN], [MF]),
        Chord.from_lists([D4, A4, BF4], [HN], [MF]),
    ]

    rpb: list[Chord] = [
        Chord.from_lists([E5, F5, A5], [WN], [MF]),
        Chord.from_lists([D5, E5, G5], [HN], [MF]),
        Chord.from_lists([E5, F5, A5], [HN], [MF]),
        Chord.from_lists([D5, E5, G5], [HN], [MF]),
        Chord.from_lists([D5, E5, G5], [HN], [MF]),
        Chord.from_lists([D5, E5, F5], [HN], [MF]),
        Chord.from_lists([A4, D5, E5], [WWN + WN], [MF]),
    ]

    # double chord by copying notes up one octave
    for index in range(len(rpa)):
        rpa[index].add_notes(mods.octave(rpa[index].notes))

    for index in range(len(rpb)):
        rpb[index].add_notes(mods.octave(rpb[index].notes))

    right_part = Phrase()
    right_part.add_rest(HN)
    right_part.add_notes(rpa)
    right_part.add_rest(BREATH)
    right_part = mods.repeat_phrase(right_part, 2)
    right_part.add_rest(HN)
    right_part.add_notes(rpb)
    right_part.add_rest(BREATH)

    left_part = Phrase()
    left_part.add_chord_by_lists([D1, D2, D3], [WN], [MF])
    left_part.add_chord_by_lists([C1, C2, C3], [WN], [MF])
    left_part.add_chord_by_lists([BF0, BF1, BF2], [WN], [MF])
    left_part.add_rest(BREATH)
    left_part = mods.repeat_phrase(left_part, 2)

    left_part.add_chord_by_lists([A0, A1, A2], [WN], [MF])
    left_part.add_chord_by_lists([A0, A2, A3], [WWN + WN + WWN + WN], [MF], [PORTATO])
    left_part.add_rest(BREATH)

    part = Part("Piano", ACOUSTIC_GRAND_PIANO)
    part.add_phrase(right_part, 0.0)
    part.add_phrase(left_part, 0.0)
    return part


def violin_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([D4, A4, E6], [WN], [MF])
    phrase_a.add_note(Note(F6, HN, MF))
    phrase_a.add_note(Note(D4, HN, MF))
    phrase_a.add_chord_by_lists([D4, D5, D6], [HN], [MF])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([D4, A4, A6], [WN], [MF])
    phrase_b.add_chord_by_lists([A4, G6], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, A6], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, G6], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, G6], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, F6], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, E6], [WWN + WN], [MF])
    phrase_b.add_rest(BREATH)

    return Part("Violins", STRING_ENSEMBLE, [phrase_a, phrase_a, phrase_b])


def viola_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_rest(HN)
    phrase_a.add_chord_by_lists([D4, E5], [WN], [MF])
    phrase_a.add_chord_by_lists([D4, F5], [HN], [MF])
    phrase_a.add_chord_by_lists([D4, D5], [HN], [MF])
    phrase_a.add_chord_by_lists([D4, D5], [HN], [MF])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_rest(HN)
    phrase_b.add_chord_by_lists([D4, A4, E5], [WN], [MF])
    phrase_b.add_chord_by_lists([D4, D5], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, E5], [HN], [MF])
    phrase_b.add_chord_by_lists([D4, D5], [HN], [MF])
    phrase_b.add_chord_by_lists([D4, D5], [HN], [MF])
    phrase_b.add_chord_by_lists([D4, A4, A5], [HN], [MF])
    phrase_b.add_chord_by_lists([A4, E5], [WWN + WN], [MF])
    phrase_b.add_rest(BREATH)

    return Part("Viola", STRING_ENSEMBLE, [phrase_a, phrase_a, phrase_b])


def cello_db_part() -> Part:
    phrase_a = Phrase()
    phrase_a.add_chord_by_lists([D2, D3], [WN], [MF])
    phrase_a.add_chord_by_lists([C2, C3], [WN], [MF])
    phrase_a.add_chord_by_lists([BF1, BF2], [WN], [MF])
    phrase_a.add_rest(BREATH)

    phrase_b = Phrase()
    phrase_b.add_chord_by_lists([A2, A1], [WN], [MF])
    phrase_b.add_chord_by_lists([A3, A2], [WWN + WN + WWN + WN], [MF])
    phrase_b.add_rest(BREATH)

    return Part("Cello&Bass", STRING_ENSEMBLE, [phrase_a, phrase_a, phrase_b])


def make_score() -> Score:
    parts = [
        flute_part(),
        oboe_part(),
        clarinet_part(),
        bassoon_part(),
        horn_part(),
        trumpet_part(),
        trombone_part(),
        tuba_part(),
        timpani_part(),
        choir_part(),
        piano_part(),
        violin_part(),
        viola_part(),
        cello_db_part(),
    ]

    # set channels for each part
    # channel 9 (midi channel 10) is reserved for percussion and is not used
    # here. you can use the `PERCUSSION_CHANNEL` constant instead of `9`
    channel_index = 0
    for part in parts:
        if channel_index == PERCUSSION_CHANNEL:
            channel_index += 1
        part.channel = channel_index
        channel_index += 1

    return Score(
        "Carmina Burana: 1. O Fortuna",
        parts=parts,
        tempo=120,
    )


if __name__ == "__main__":
    # create the score
    score = make_score()

    # create a sound font player, pass a path the a sound font 2 file
    SF2 = "soundfonts/my_soundfont.sf2"

    # this song uses a lot of instruments which can get very loud
    # use the `gain` parameter to adjust the base sound level
    player = SfPlayer(SF2, gain=-3)

    # play the score
    # put this inside a try/except block to prevent backtrace on keyboard interrupt
    try:
        player.play_score(score)
        # let remaining notes ring
        sleep(1)
    except KeyboardInterrupt:
        print("stopped")

    del player
