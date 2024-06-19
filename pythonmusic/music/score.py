from ..constants.tempo import MODERATO as _MODERATO
from .part import Part


class Score:
    """A score represents a music piece."""

    def __init__(
        self,
        title: str | None,
        parts: list[Part] = [],
        tempo: float = _MODERATO,
    ) -> None:
        self.title = title
        self.parts = []
        self.tempo = tempo

        self.add_parts(parts)

    def __len__(self) -> int:
        return self.parts.__len__()

    def __str__(self) -> str:
        title_str = f"{self.title}, " if self.title is not None else ""
        parts_str = f"{len(self.parts)} Parts"
        return f"Score({title_str}, {parts_str}, {self.tempo})"

    def length(self) -> int:
        """Returns the number of of parts in the score."""
        return len(self)

    def duration(self) -> float:
        """Returns the unit length of the score."""
        if len(self.parts) == 0:
            return 0
        return max(map(lambda part: part.duration(), self.parts))

    def has_part(self, part: Part) -> bool:
        """Returns `True` if the given part is in the score."""
        for part_in in self.parts:
            if part == part_in:
                return True
        return False

    def add_part(self, part: Part):
        """
        Adds the given part to the score.

        Unlike phrases and notes, parts may only be added once to a score.

        :param Part part: The part to add
        :raises ValueError: If the part to add is already present in the score
        """

        if self.has_part(part):
            raise ValueError("Part has already been added to the score")
        self.parts.append(part)

    def add_parts(self, parts: list[Part]):
        """
        Adds the given parts to the score.

        Unlike phrases and notes, parts may only be added once to a score.

        :param list[Part] parts: The part to add
        :raises ValueError: If any part to add is already present in the score
        """

        for part in parts:
            # there is no benefit in not doing this
            self.add_part(part)

    def remove_part(self, part: Part):
        """
        Removes the given part from the score.

        :param Part part: The part to be removed
        :raises ValueError: If the given part is not in the score
        """
        for index, part_in in enumerate(self.parts):
            if part_in is part:
                self.parts.pop(index)
                return
        raise ValueError("Part is not in score")

    def remove_part_by_index(self, index: int) -> Part:
        """
        Removes the part at the given index. Returns the removed part.

        :param int index: The index of the part to remove
        :raises IndexError: If the given index in invalid
        """

        return self.parts.pop(index)

    def clear(self):
        """Removes all parts from the score."""
        self.parts = []
