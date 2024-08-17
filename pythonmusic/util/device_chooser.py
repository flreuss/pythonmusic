from typing import TypeVar
from pythonmusic.io import get_midi_senders, get_midi_receivers

_PromptElement = TypeVar("_PromptElement")


def user_list_prompt(choices: list[_PromptElement]) -> _PromptElement | None:
    # if the input is empty, return None
    if len(choices) == 0:
        return None
    # if we have only one choice, return that
    if len(choices) == 1:
        return choices[0]

    # repeat user prompt until choice is made
    choice: _PromptElement | None = None
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


def user_receiver_prompt() -> str | None:
    """
    Retrieves open midi receivers and asks user to choose one if more than one
    option is available.

    Returns `None` if no ports are available.
    """

    receivers = get_midi_receivers()
    receiver_name = user_list_prompt(receivers)
    return receiver_name


def user_sender_propt() -> str | None:
    """
    Retrieves open midi senders and asks user to choose one if more than one
    option is available.

    Returns `None` if no ports are available.
    """

    senders = get_midi_senders()
    sender_name = user_list_prompt(senders)
    return sender_name
