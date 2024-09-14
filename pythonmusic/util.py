# util.py
#
# Utility functionality. All functions here have no dependencies in the parent
# library. Use `helpers` if you need to import

from typing import TypeVar

__all__ = [
    "Number",
    "assert_range",
    "make_instrument",
    "instrument_get_patch_bank",
]

Number = TypeVar("Number", int, float)
"""A type that is either a float or an integer."""


def assert_range(value: Number, lower: Number, upper: Number):
    """
    Asserts that the given value is at least `lower` and at most `upper`.
    The upper range is included.

    Args:
        value (Number): A base valse
        lower (Number): The lower bound of the valid range
        upper (Number): The upper bound of the valid range

    Raises:
        ValueError: If `value` is not in range from `lower` to `upper` (inclusive)
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

    For mor information, see
    `General MIDI Level 2 <https://en.m.wikipedia.org/wiki/General_MIDI_Level_2>`.

    Args:
        patch (int): The instrument base id in range 1..=127.
        bank (int): TJkhe instruments variation bank in range 0..=9.

    Returns:
        int: A composite integer containing the patch in the lower and the
        variation bank in the upper byte.
    """
    assert_range(patch, 1, 128)
    assert_range(bank, 0, 128)
    return (bank << 8) | patch


def instrument_get_patch_bank(instrument: int) -> tuple[int, int]:
    """
    Returns the patch and bank ids for the given instrument.
    The input is assumed to be valid.

    Args:
        instrument (int): A valid instrument as created by `make_instrument()`.

    Returns:
        tuple[int, int]: A tuple containing the instrument's patch and bank.
    """
    BYTE = 0b11111111
    patch = instrument & BYTE
    bank = (instrument >> 8) & BYTE

    assert_range(patch, 1, 128)
    assert_range(bank, 0, 128)
    return (patch, bank)
