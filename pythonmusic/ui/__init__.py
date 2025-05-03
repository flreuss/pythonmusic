try:
    import tkinter as _

    from .window import *


except ImportError:
    from sys import stderr

    print("Cannot import module 'tkinter'; ui module cannot be provided")

    pass

# __all__ = ["Window"]
__all__ = []
