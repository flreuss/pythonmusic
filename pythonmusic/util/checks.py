from typing import TypeVar


IF = TypeVar("IF", int, float)


def assert_range(value: IF, lower: IF, upper: IF):
    """
    Asserts that the given value is at least `lower` and at most `upper`.
    The upper range is included.
    """
    if value < lower or value > upper:
        raise ValueError(
            f"given value {value} is outside allowed bounds of {lower} and {upper}"
        )
    return
