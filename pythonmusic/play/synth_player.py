from collections.abc import Callable
from time import sleep


class SynthPlayer:
    def __init__(self):
        pass

    @staticmethod
    def _wait(interval: float, should_terminate: Callable[[], bool]):
        """
        Prompts the player to wait, polling on every `interval` seconds
        `should_terminate` to check if function should continue waiting.
        """
        while not should_terminate():
            sleep(interval)
