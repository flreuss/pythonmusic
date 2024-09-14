from pythonmusic.constants.tempo import MODERATO
from pythonmusic.music.part import Part

__all__ = ["Score"]


class Score:
    """
    A score represents a music piece.

    Args:
        title (str | None): The title of the score. Defaults `None`
        parts (list[Part]): A list of parts. Can be added later
    """

    def __init__(
        self,
        title: str | None,
        parts: list[Part] = [],
        tempo: float = MODERATO,
    ) -> None:
        self.title: str | None = title
        self.parts: list[Part] = []
        self.tempo: float = tempo

        self.add_parts(parts)

    def __len__(self) -> int:
        return self.parts.__len__()

    def length(self) -> int:
        """The number of of parts in the score."""
        return len(self)

    def duration(self) -> float:
        """The unit length of the score."""
        return (
            max(map(lambda part: part.duration(), self.parts))
            if len(self.parts) != 0
            else 0
        )

    def has_part(self, part: Part) -> bool:
        """
        Returns `True` if the given part is in the score.

        Args:
            part (Part): The part to search for

        Returns:
            bool: `True` if the part was found, otherwise `False`
        """
        for part_in in self.parts:
            if part == part_in:
                return True
        return False

    def add_part(self, part: Part):
        """
        Adds the given part to the score.

        Unlike phrases and notes, parts may only be added once to a score.

        Args:
            part (Part): The part to add

        Raises:
            ValueError: If part already exists in the score
        """

        if self.has_part(part):
            raise ValueError("Part has already been added to the score")
        self.parts.append(part)

    def add_parts(self, parts: list[Part]):
        """
        Adds the given parts to the score.

        Unlike phrases and notes, parts may only be added once to a score.

        Args:
            parts (list[Part]): The parts to add

        Raises:
            ValueError: If any of the parts are duplicates or already present in
                the score
        """

        for part in parts:
            # there is no benefit in not doing this
            self.add_part(part)

    def remove_part(self, part: Part):
        """
        Removes the given part from the score.

        Args:
            part (Part): The part to be removed

        Raises:
            ValueError: If given part does not exist in the score
        """
        for index, part_in in enumerate(self.parts):
            if part_in is part:
                self.parts.pop(index)
                return
        raise ValueError("Part is not in score")

    def remove_part_by_index(self, index: int) -> Part:
        """
        Removes the part at the given index. Returns the removed part.

        Raises:
            IndexError: If the given index is invalid

        Args:
            index (int): The index of the part to remove

        Returns:
            Part: The removed Part
        """

        return self.parts.pop(index)

    def clear(self):
        """Removes all parts from the score."""
        self.parts = []
