from .note import Note

# TODO: convert to abstract class or similar


class NoteCollection:
    def __init__(self, notes: list[Note]) -> None:
        self.notes = []
        self.add_notes(notes)

    def __len__(self) -> int:
        return self.notes.__len__()

    def duration(self) -> float:
        """Returns the total unit length of this collection."""
        return
