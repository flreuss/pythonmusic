from abc import ABC as _ABC
from abc import abstractmethod as _abstractmethod


class PhraseElement(_ABC):
    @property
    @_abstractmethod
    def duration(self) -> float:
        pass

    # the following two methods are overwritten in sub classes
    # this is a messy solution to circular import while using the type checker
    @_abstractmethod
    def is_chord(self) -> bool:
        pass

    @_abstractmethod
    def is_note(self) -> bool:
        pass
