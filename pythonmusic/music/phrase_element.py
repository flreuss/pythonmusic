from abc import ABC
from abc import abstractmethod

__all__ = ["PhraseElement"]


class PhraseElement(ABC):
    @property
    @abstractmethod
    def duration(self) -> float:
        pass

    # the following two methods are overwritten in sub classes
    # this is a messy solution to circular import while using the type checker
    @abstractmethod
    def is_chord(self) -> bool:
        pass

    @abstractmethod
    def is_note(self) -> bool:
        pass
