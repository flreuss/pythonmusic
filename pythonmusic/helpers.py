from typing import Any, Callable, Optional
from math import floor

from pythonmusic.io import get_midi_senders, get_midi_receivers
from pythonmusic.util import assert_range, Number

__all__ = [
    "user_list_prompt",
    "user_receiver_prompt",
    "user_sender_propt",
    "map_value",
    "map_scale",
]


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
    # if the input is empty, return None
    if len(choices) == 0:
        return None
    # if we have only one choice, return that
    if len(choices) == 1:
        return choices[0]

    # repeat user prompt until choice is made
    choice: Optional[Any] = None
    while choice is None:
        # This leverages Python's principle of asking for forgiveness instead of
        # permission. Instead of checking if user input is valid, we try to
        # convert an handle the error, if necessary.
        try:
            # print options for user
            for index, option in enumerate(choices):
                print(f" [{index}] : {option}")

            # prompt user for input
            user_input = input("(int) > ")
            # convert input (str) to integer; this can fail with a ValueError if
            # the given input cannot be represented as an int
            index = int(user_input)
            # index choices with the index; this can fail with an IndexError if
            # the given index is out of bounds
            choice = choices[index]

        except ValueError:
            # here we tried to convert something into an integer that cant be
            # converted
            print("Input was not an integer\n")

        except IndexError:
            # the given input was converted into an integer, but the integer was
            # out of bounds
            print("Input was out of range\n")

    return choice


def user_receiver_prompt() -> Optional[str]:
    """
    Retrieves open midi receivers and asks user to choose one if more than one
    option is available.

    Returns:
        Optional[str]: The user's choice of receiver. `None` if no ports are available.
    """

    receivers = get_midi_receivers()
    receiver_name = user_list_prompt(receivers)
    return receiver_name


def user_sender_propt() -> Optional[str]:
    """
    Retrieves open midi senders and asks user to choose one if more than one
    option is available.

    Returns:
        Optional[str]: The user's choice of sender. `None` if no ports are available.
    """

    senders = get_midi_senders()
    sender_name = user_list_prompt(senders)
    return sender_name


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

    If you map an `integer`, you may define a conversion strategy. Internally,
    all values are converted into floats. If the output type is an `integer`, the
    given `conversion_strategy` is used to convert the result. By default, this
    uses Python's build-in `round()` function. You may also want to use
    `floor()`. This is optional.

    Args:
        value (Number): A base value
        min_value (Number): Defines lower bound of input range
        max_value (Number): Defines upper bound of input range
        min_result (Number): Defines lower bound of result range
        min_result (Number): Defines upper bound of result range
        conversion_strategy (Callable[[float], int]): A function that converts a float to an int

    Returns:
        int | float: The mapped value
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
