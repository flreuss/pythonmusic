from pythonmusic.music import PhraseElement, Note


# TODO: find shorter function name
def sharp(pitch: int) -> int:
    """Returns the given pitch raised by one. This is equivalent to `pitch + 1`."""
    return pitch + 1


def flat(pitch: int) -> int:
    """Returns the given pitch lowered by one. This is equivalent to `pitch - 1`."""
    return pitch - 1


def dotted(duration: float, dots: int = 1) -> float:
    """Calculates the length of a dotted note."""
    # out = duration
    # dot = duration * 0.5
    # for i in range(dots):
    #     out += dot
    #     dot *= 0.5
    # return out
    if dots < 1:
        return duration
    return duration * (2 - (0.5**dots))


def legato(notes: list[Note]) -> list[Note]:
    """Adds legato to all given notes."""
    return list(map(lambda note: note.with_legato(), notes))
