from collections.abc import Sequence
from math import floor
from typing import TypeVar


_RangeScalar = TypeVar("_RangeScalar", int, float)


def assert_range(value: _RangeScalar, lower: _RangeScalar, upper: _RangeScalar):
    """
    Asserts that the given value is at least `lower` and at most `upper`.
    The upper range is included.
    """
    if value < lower or value > upper:
        raise ValueError(
            f"given value {value} is outside allowed bounds of {lower} and {upper}"
        )
    return


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


def bpm_to_mspb(bpm: float) -> int:
    """
    Converts beats per minute to milliseconds per beat.
    """
    # (60 / bpm) * 1_000
    return floor(60_000 / bpm)


def mspb_to_bpm(mspb: int) -> float:
    """
    Converts milliseconds per beat to beats per minute.
    """
    return floor(60_000 / mspb)
