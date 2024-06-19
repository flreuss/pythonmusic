from .phrase import Phrase
from pythonmusic.constants.panning import PAN_CENTER as _PAN_CENTER
from pythonmusic.constants.instruments import (
    ACOUSTIC_GRAND_PIANO as _ACOUSTIC_GRAND_PIANO,
)


class Part:
    """A part represents an instrument and consists of phrases."""

    # TODO: Check if channel 1 should be default channel
    def __init__(
        self,
        title: str | None,
        instrument: int = _ACOUSTIC_GRAND_PIANO,
        channel: int = 1,
        phrases: list[Phrase] = [],
        panning: int = _PAN_CENTER,
    ) -> None:
        self.title: str | None = title
        self.instrument: int = instrument
        self.channel: int = channel
        self.phrases: list[Phrase] = phrases
        self.panning: int = panning
