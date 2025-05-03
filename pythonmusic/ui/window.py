import tkinter as tk

from .widget import Widget

__all__ = ["Window"]


class Window:
    """
    A single window.

    PythonMusic's UI module is a thin wrapper around Python Tk. This is done to
    provide an easier way to manage and create ui. That being said, for simplicity's
    sake, many features are missing, simplified, or omitted. Either use Tk directly,
    or call this class' `raw()` method, which returns the Tk root widget.
    """

    def __init__(self, title: str, width: int, height: int):
        self._root = tk.Tk(baseName=title, className="pythonmusic.ui")

    def raw(self) -> tk.Tk:
        """
        Returns the internal raw Tk handle.
        """
        return self._root

    def add_widget(self, widget: Widget):
        widget.make(self._root)
        widget.raw().pack()

    def run(self):
        """
        Run the main loop of the window i.e. opens it.
        """
        self._root.mainloop()
