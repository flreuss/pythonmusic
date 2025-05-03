import tkinter as tk
from abc import ABC, abstractmethod

__all__ = ["Widget"]


class Widget(ABC):

    @abstractmethod
    def raw(self) -> tk.Widget: ...

    @abstractmethod
    def make(self, root: tk.Tk): ...
