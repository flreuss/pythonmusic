# util.py
#
# Utility functionality. All functions here have no dependencies in the parent
# library. Use `helpers` if you need to import

from math import floor, log
from time import sleep
from typing import Any, Callable, Optional, TypeVar

__all__ = [
    "block",
    "Number",
    "assert_range",
    "clip",
    "make_instrument",
    "instrument_get_patch_bank",
    "find_pattern",
    "find_pattern_index",
    "map_value",
    "map_scale",
    "user_list_prompt",
    "mpqn_to_bpm",
    "bpm_to_mpqn",
    "bpm_to_sec",
    "sec_to_bpm",
    "beats_to_ticks",
    "frequency_to_key",
    "key_to_frequency",
    "contains_identity",
    "int_to_vlq",
    "vlq_to_int",
    "seconds_to_samples",
    "samples_to_seconds",
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


def clip(value: Number, lower: Number, upper: Number):
    """
    Clips a value to a range.

    Returns the lower bound if `value < lower`, or the upper bound if `value >
    upper`; otherwise `value`.

    Args:
        value(Number): A value
        lower(Number): The lower bound
        upper(Number): The upper bound

    Returns:
        Number: The clipped value
    """
    return min(upper, max(lower, value))


def make_instrument(patch: int, bank: int = 0) -> int:
    """
    Creates the internal int representation of an instrument.
    Normally, assigning an int directly is fine, use this function if you need
    to assign the bank value only.

    For more information, see
    `General MIDI Level 2 <https://en.m.wikipedia.org/wiki/General_MIDI_Level_2>`_.

    Args:
        patch (int): The instrument base id in range from 1 to 127.
        bank (int): The instruments variation bank in range from 0 to 127.

    Returns:
        int: A composite integer containing the patch in the lower and the
        variation bank in the upper byte.
    """
    assert_range(patch, 0, 127)
    assert_range(bank, 0, 127)
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

    assert_range(patch, 0, 128)
    assert_range(bank, 0, 128)
    return (patch, bank)


def find_pattern(pattern: str, lines: list[str]) -> Optional[str]:
    """
    Searches the given lines for a pattern.

    Args:
        pattern(str): A pattern to search for
        lines(list[str]): A list of strings to search

    Returns:
        Optional[str]: The first line that contains the given pattern, or `None`
            if no matches found.
    """

    for line in lines:
        if pattern in line:
            return line

    return None


def find_pattern_index(pattern: str, lines: list[str]) -> Optional[int]:
    """
    Searches the given lines for a pattern and returns matching index.

    Args:
        pattern(str): A pattern to search for
        lines(list[str]): A list of strings to search

    Returns:
        Optional[int]: The index of the first line that contains the pattern, or
            `None` if no matches found.
    """

    for index, line in enumerate(lines):
        if pattern in line:
            return index

    return None


def map_value(
    value: Number,
    min_value: Number,
    max_value: Number,
    min_result: Number,
    max_result: Number,
    conversion_strategy: Callable[[float], int] = round,
) -> int | float:
    """
    Maps a given value from one range onto another.

    The input parameters define two ranges and a value. The position of the given
    value is mapped relative to the source mapping onto the target mapping.

    If you map a value onto an integer range, you may define a conversion
    strategy. This function receives a float as input and converts it
    to an integer. By default, it uses Python's built-in `round()` function,
    which rounds to the nearest integer. However, you may also want to use
    `math.floor()`, which always rounds down, or define your own function:

    .. code-block:: python

        from pythonmusic import *
        import math

        # conversion strategy converts a float to an int
        def my_conversion(v: float) -> int:
            base = math.floor(v)  # discard decimals
            decimals = v % 1.0

            # only return next-higher integer, if we are at
            # .8 or higher
            if decimals >= 0.8:
                return base + 1
            else:
                return base

        pitch = map_value(0.34, 0.0, 1.0, A3, A4, my_conversion)

    Args:
        value (Number): A base value
        min_value (Number): Defines lower bound of input range
        max_value (Number): Defines upper bound of input range
        min_result (Number): Defines lower bound of result range
        min_result (Number): Defines upper bound of result range
        conversion_strategy (Callable[[float], int]): A function that converts a float to an int

    Returns:
        Number: The mapped value
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

    return (
        conversion_strategy(result)
        if type(max_result) == int or type(min_result) == int
        else result
    )


def map_scale(
    value: Number,
    min_value: Number,
    max_value: Number,
    min_result: int,
    max_result: int,
    scale: list[int],
    root: Optional[int] = None,
) -> int:
    """
    Maps a given value from on range to another on the given scale.

    The result returned is guaranteed to be on the given scale. Unlike
    `map_value`, this function is intended to be used with note pitches and will
    always return an integer.

    Args:
        value (Number): A base value
        min_value (Number): Defines lower bound of input range
        max_value (Number): Defines upper bound of input range
        min_result (int): Defines lower bound of result range
        min_result (int): Defines upper bound of result range
        scale (list[int]): A list of integers that represent interval offsets
            from a root
        root (Optional[int]): A base pitch that represent the base offset. Defaults
            to `min_value`

    Returns:
        Number: The mapped value
    """
    assert_range(value, min_value, max_value)
    assert min_value <= max_value
    assert min_result <= max_result

    for pitch in scale:
        assert_range(pitch, 0, 11)

    if len(scale) < 1:
        raise ValueError("Given scale must contain at least one value")

    # if base is not given, default to `min_result`
    root = root or min_result

    # length of scale, not all scales have 11 notes
    scale_len = len(scale)

    # map input onto target range
    mapped = map_value(float(value), min_value, max_value, min_result, max_result)
    # align with scale (no offset/key)
    aligned = mapped - root

    # normalise range
    normalised = aligned * scale_len / 12

    # calculate octave and step offset, this is equivalent to div with remainder
    octave = floor(normalised / scale_len)
    step = floor(normalised % scale_len)
    index = step

    # finally assemble result
    # all parts are integers, but scale and base may not be; convert
    return int((octave * 12) + scale[index] + root)


def user_list_prompt(choices: list[Any]) -> Optional[Any]:
    """
    Prompts the user to choose an option from a given number of choices.

    Does not ask the user for input if the number of choices is smaller than
    `1`.

    Args:
        choices (list[Any]): A number of options for the user to choose from.

    Returns:
        The user's choice, `choices[0]` if `len(choices) == 1`, or `None` if
        empty
    """
    if len(choices) == 0:
        return None

    if len(choices) == 1:
        return choices[0]

    choice: Optional[Any] = None
    while choice is None:
        try:
            for index, option in enumerate(choices):
                print(f" [{index}] : {option}")

            user_input = input("(int) > ")
            index = int(user_input)
            choice = choices[index]

        except ValueError:
            print("Input was not an integer\n")

        except IndexError:
            print("Input was out of range\n")

    return choice


def bpm_to_mpqn(bpm: Number) -> int:
    """
    Converts BPM to MpQN.

    This function is used to convert a tempo given in beats per minute to the
    midi-standard microseconds per quarter note.

    Args:
        bpm(Number): Beats per minute

    Returns:
        int: Microseconds per quarter note
    """
    return round(60_000_000.0 / float(bpm))


def mpqn_to_bpm(mpqn: Number) -> float:
    """
    Converts MpQN to BPM.

    This function is used to convert a tempo given in microseconds per quarter
    note to beats per minute.

    Args:
        mpqn(Number): Microseconds per quarter note

    Returns:
        float: Beats per minute
    """

    return 60_000_000.0 / float(mpqn)


def bpm_to_sec(bpm: Number) -> float:
    """
    Converts BPM to the duration per beat in seconds.

    Args:
        bpm(Number): Beats per minute

    Returns:
        float: Seconds per beat
    """

    return 60.0 / float(bpm)


def sec_to_bpm(sec: Number) -> float:
    """
    Converts the duration of a beat in seconds to BPM.

    Args:
        sec(Number): Duration of beat in seconds

    Returns:
        float: Beats per minute
    """

    return 60.0 / float(sec)


def beats_to_ticks(beats: float, ppq: int) -> int:
    """
    Converts beats to midi ticks.

    Use this function to convert a duration given in beats to midi ticks.
    The `ppq` property should be set to the library's default of `96` pulses
    per quarter.

    Args:
        beats(float): Beats to convert
        ppq(int): Tick resolution per quarter note. Should be set to `96`
    """

    return round(beats * float(ppq))


A4: int = 69
TUNING_PITCH: float = 440.0


def frequency_to_key(frequency: float) -> int:
    """
    Returns the closest well-tempered key for the given frequency.

    Args:
        pitch(float): A frequency

    Returns:
        float: A well-tempered key
    """
    return round((12 * log(frequency / TUNING_PITCH, 2)) + A4)


def key_to_frequency(key: int) -> float:
    """
    Returns the frequency for the given well-tempered key.

    Args:
        key(int): A key

    Returns:
        float: A frequency
    """
    return pow(2, (key - A4) / 12) * TUNING_PITCH


def contains_identity(input: list[Any], item: Any) -> bool:
    """
    Checks if a list contains the given item by their identity, not equality.

    Args:
        input(list[Any]): A list of any object
        item(Any): Any object

    Returns:
        bool: `True`, if the list contains a reference to the object, `False`
            otherwise
    """

    for list_item in input:
        if list_item is item:
            return True

    return False


def int_to_vlq(input: int) -> bytes:
    """
    Converts an integer to a variable length quantity (vlq).

    For more information on vlq, see the :doc:`midi <../appendix/midi>` appendix.

    Args:
        input(int): An integer

    Returns:
        bytes: vlq
    """
    if input == 0:
        # wow, bytes(n) is [0x00] * n bytes, bytes(0) ~ []
        # read the docs, dummy; this messed with the entire export
        # why is it always a one-liner?
        return bytes(1)

    # check if input is < 0
    if input < 0:
        raise ValueError("Cannot convert negative integer")

    # check if input is below max
    MAX = 0x0FFFFFFF
    if input > MAX:
        raise ValueError(f"Exceeded maximum value {input} > {MAX}")

    # drain input
    output = bytearray()
    while input > 0:
        output.append(0b10000000 | (0b01111111 & input))
        input >>= 7

    # set clear msb
    output[0] = output[0] & 0b01111111
    return bytes(reversed(output))


def vlq_to_int(input: bytes) -> int:
    """
    Converts a variable length quantity (vlq) to an integer.

    For more information on vlq, see the :doc:`midi <../appendix/midi>` appendix.

    Args:
        input(bytes): A vlq

    Returns:
        int: An integer
    """
    output = 0

    for byte in input:
        output <<= 7
        output |= byte & 0b01111111

    return output


def block(interval: float = 1.0, condition: Optional[Callable[[], bool]] = None):
    """
    Blocks execution of the current thread.

    Use this function to keep players, targets, and midi ports alive in the
    background.

    You can define a callback function that decides if the block should end. The
    callback should return `True` if the block should continue, `False`
    otherwise.

    Args:
        interval(float): Interval in seconds after which the condition is
            checked
        condition(Optional[Callable[[None], bool]]): A callback that returns
            `True` if the block should continue, or `False` otherwise
    """

    try:
        while True:
            if condition and condition():
                break
            else:
                sleep(interval)
    except KeyboardInterrupt:
        pass


def seconds_to_samples(duration: Number, sample_rate: Number) -> int:
    """
    Returns the number of samples for a duration at the given smaple rate.

    This function exists to communicate what is being done. Essentially, this
    boils down to `duration * sample_rate`.

    Args:
        duration(Number): The duration in seconds
        sample_rate(Number): The sample rate in samples per second

    Returns:
        int: Number of samples
    """
    return round(float(duration) * float(sample_rate))


def samples_to_seconds(samples: int, sample_rate: Number) -> float:
    """
    Returns the duration of the given sample count at `sample_rate` in seconds.

    Args:
        samples(int): Sample count
        sample_rate(Number): Current sampe rate

    Return:
        float: Duration is seconds
    """
    return float(samples) / float(sample_rate)
