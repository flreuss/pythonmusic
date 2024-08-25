# util.py
#
# Utility functionality. All functions here have no dependencies in the parent
# library. Use `helpers` if you need to import

from collections.abc import Callable
from math import floor


Number = int | float
"""A type that is either a float or an integer."""


def assert_range(value: Number, lower: Number, upper: Number):
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
    BYTE = 0b11111111
    patch = instrument & BYTE
    bank = (instrument >> 8) & BYTE
    return (patch, bank)


def map_value(
    value: Number,
    min_value: Number,
    max_value: Number,
    min_result: Number,
    max_result: Number,
    conversion_strategy: Callable[[float], int] = round,
) -> Number:
    """
    Maps a given value from one range onto another.

    The input parameters define two ranges and a value. The position of the given
    value is mapped relative to the source mapping onto the target mapping.

    If you map an `integer`, you may define a conversion strategy. Internally,
    all values are converted into floats. If the output type is an `integer`, the
    given `conversion_strategy` is used to convert the result. By default, this
    uses Python's build-in `round()` function. You may also want to use
    `floor()`.

    :param value: A base value
    :param min_value: Defines lower bound of input range
    :param max_value: Defines upper bound of input range
    :param min_result: Defines lower bound of result range
    :param min_result: Defines upper bound of result range
    :param conversion_strategy: A function that converts a float to an int
    """
    # assert that all given values are in bounds
    assert_range(value, min_value, max_value)
    assert min_value <= max_value
    assert min_result <= max_result

    delta_value = max_value - min_value
    offset_value = value - min_value
    delta_result = max_result - min_result

    # Python3 converts to float automatically
    multiplyer = offset_value / delta_value
    result = (delta_result * multiplyer) + min_result

    return conversion_strategy(result) if type(value) == int else result


def map_scale(
    value: Number,
    min_value: Number,
    max_value: Number,
    min_result: int,
    max_result: int,
    scale: list[int],
    base: int | None = None,
) -> int:
    """
    Maps a given value from on range to another on the given scale.

    The result returned is guaranteed to be on the given scale. Unlike
    `map_value`, this function is intended to be used with note pitches and will
    always return an integer.

    :param value: A base value
    :param min_value: Defines lower bound of input range
    :param max_value: Defines upper bound of input range
    :param min_result: Defines lower bound of result range
    :param min_result: Defines upper bound of result range
    :param scale: A list of integers that represent interval offsets from a root
    :param base: A base pitch that represents offset `0`. Defaults to `min_value`
    """
    assert_range(value, min_value, max_value)
    assert min_value <= max_value
    assert min_result <= max_result

    for pitch in scale:
        assert_range(pitch, 0, 11)

    if len(scale) < 1:
        raise ValueError("Given scale must contain at least one value")

    # if base is not given, default to `min_result`
    base = base or min_result

    # length of scale, not all scales have 11 notes
    scale_len = len(scale)

    # map input onto target range
    mapped = map_value(float(value), min_value, max_value, min_result, max_result)
    # align with scale (no offset/key)
    aligned = mapped - base

    # normalise range
    normalised = aligned * scale_len / 12

    # calculate octave and step offset, this is equivalent to div with remainder
    octave = floor(normalised / scale_len)
    step = floor(normalised % scale_len)
    index = step

    # finally assemble result
    # all parts are integers, but scale and base may not be; convert
    return int((octave * 12) + scale[index] + base)
