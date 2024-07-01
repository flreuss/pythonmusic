from pythonmusic.util.checks import assert_range


def make_instrument(patch: int, bank: int = 0) -> int:
    """
    Creates the internal int representation of an instrument.
    Normally, assigning an int directly is fine, use this function if you need
    to assign the bank value only.

    For mor information, see (General MIDI Level 2)[https://en.m.wikipedia.org/wiki/General_MIDI_Level_2].

        Parameters:
            patch (int): The instrument base id in range 1..=127.
            bank (int): TJkhe instruments variation bank in range 0..=9.

        Returns:
            A composite integer containing the patch in the lower and the
            variation bank in the upper byte.
    """
    assert_range(patch, 1, 128)
    # TODO: Check if 9 really is the highest-used bank; consider just unlocking this
    assert_range(bank, 0, 9)
    return (bank << 8) | patch


def instrument_get_patch_bank(instrument: int) -> tuple[int, int]:
    # TODO: Add links to pydoc
    """
    Returns the patch and bank ids for the given instrument.
    The input is assumed to be valid.

        Parameters:
            instrument (int): A valid instrument as created by `make_instrument()`.

        Returns:
            A tuple containing the instrument's patch and bank.
    """
    # TODO: add validation
    BYTE = 0x11111111
    patch = instrument & BYTE
    bank = (instrument >> 8) & BYTE
    return (patch, bank)


# def triplet()
