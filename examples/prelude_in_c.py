from pythonmusic import *


def left_part() -> Part:
    """
    Returns the left part of the prelude, i.e., what the left hand plays.
    """
    part = Part("left", ACOUSTIC_GRAND_PIANO, channel=2)

    # the prelude's left part consists of two held notes
    # we define this as two phrases
    #
    # first, we define the lower phrase, which only consists of half notes until
    # the end
    # the following demonstrates adding notes lists of pitches, durations, and
    # dynamic
    # fmt: off
    pitches = [
        C4, C4, C4, C4,    # 1
        B3, B3, C4, C4,    # 3
        C4, C4, C4, C4,    # 5
        B3, B3, B3, B3,    # 7
        A3, A3, D3, D3,    # 9
        G3, G3, G3, G3,    # 11
        F3, F3, F3, F3,    # 13
        E3, E3, E3, E3,    # 15
        D3, D3, G3, G3,    # 17
        C3, C3, C3, C3,    # 19
        F2, F2, FS2, FS2,  # 21
        G2, G2, AF2, AF2,  # 23
        G2, G2, G2, G2,    # 25
        G2, G2, G2, G2,    # 27
        G2, G2, G2, G2,    # 29
        G2, G2, G2, G2,    # 31
        C2, C2, C2,        # 33
        C2, C2             # 35
    ]
    # fmt: on

    # next, we define the durations of the notes
    # all notes are half notes, except the last three which are whole notes
    durations = ([HN] * (len(pitches) - 3)) + ([WN] * 3)

    # then, we define an array of dynamics
    # for simplicity, we will not have that change throughout the piece
    dynamics = [MF] * len(pitches)

    # finally, we create the phrase from the lists
    lower_phrase = Phrase([])
    lower_phrase.add_notes_by_lists(pitches, durations, dynamics)

    # now, we define the upper phrase, which is offset by a sixteenth rest
    # each note is also repeated twice
    # this is the same until shortly before the end, so we define this as a
    # function
    def upper_note(pitch: int) -> list[Note]:
        # the duration of the second note played in the left hand
        SND = DOTTED_EIGHTH_NOTE + QUARTER_NOTE
        return [Note.rest(SN), Note(pitch, SND)]

    upper_notes = (
        upper_note(E4)  # 1
        + upper_note(D4)  # 2
        + upper_note(D4)  # 3
        + upper_note(E4) * 2  # 4, 5
        + upper_note(D4)  # 6
        + upper_note(D4)  # 7
        + upper_note(C4) * 2  # 8, 9
        + upper_note(A3)  # 10
        + upper_note(B3)  # 11
        + upper_note(BF3)  # 12
        + upper_note(A3)  # 13
        + upper_note(AF3)  # 14
        + upper_note(G3)  # 15
        + upper_note(F3) * 2  # 16, 17
        + upper_note(D3)  # 18
        + upper_note(E3)  # 19
        + upper_note(G3)  # 20
        + upper_note(F3)  # 21
        + upper_note(C3)  # 22
        + upper_note(EF3)  # 23
        + upper_note(F3)  # 24
        + upper_note(F3)  # 25
        + upper_note(E3)  # 26
        + upper_note(D3)  # 27
        + upper_note(D3)  # 28
        + upper_note(EF3)  # 29
        + upper_note(E3)  # 30
        + upper_note(D3)  # 31
        + upper_note(D3)  # 32
        + upper_note(C3)  # 33
    )
    # and add them to the phrase
    upper_phrase = Phrase(upper_notes)
    # only the last three measures are missing now
    upper_phrase.add_notes(
        [
            Note.rest(SN),  # 34
            Note(C3, DEN + QN + HN),
            Note.rest(SN),  # 35
            Note(B3, DEN + QN + HN),
            Note(C3, WN),  # 36
        ]
    )

    # here, we add the phrases the part
    # the start times need to be set both to 0.0, so they play at the same time
    part.add_phrase(lower_phrase, start_time=0.0)
    part.add_phrase(upper_phrase, start_time=0.0)

    return part


def right_part() -> Part:
    """
    Returns the right part of the prelude, i.e., what the right hand plays.
    """
    part = Part("right", ACOUSTIC_GRAND_PIANO, channel=1)

    # the right part is a bit simpler in that there is only one note played at
    # the same time

    # TODO: add legato, when implemented

    return part


def make_score() -> Score:
    """
    Returns the full score.
    """
    score = Score("Prelude in C, BWV 846", tempo=ADAGIO)
    score.add_part(left_part())
    score.add_part(right_part())

    return score


def main():
    score = make_score()
    # play_score(score)
    pass


if __name__ == "__main__":
    main()
