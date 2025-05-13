from abc import ABC, abstractmethod

__all__ = ["PhraseElement"]


class PhraseElement(ABC):
    """
    An abstract class that defines methods for phrase elements such as notes and
    chords.
    """

    @property
    @abstractmethod
    def duration(self) -> float:
        """
        The vertical duration of the element.
        """
        pass

    # the following two methods are overwritten in sub classes
    # this is a messy solution to circular import while using the type checker
    @abstractmethod
    def is_chord(self) -> bool:
        """
        Returns `True` if the phrase element is a chord.
        """
        pass

    @abstractmethod
    def is_note(self) -> bool:
        """
        Returns `True` if the phrase element is a note.
        """
        pass
