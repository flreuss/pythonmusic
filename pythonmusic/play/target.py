from abc import ABC
from os.path import abspath, expanduser
from typing import Optional, override

from tinysoundfont import Synth as TsfSynth

import pythonmusic.constants.messages as mm
from pythonmusic.constants import PERCUSSION_CHANNEL
from pythonmusic.constants.control_change import BANK_CHANGE
from pythonmusic.constants.instruments import ACOUSTIC_GRAND_PIANO
from pythonmusic.midi.io import MidiOut
from pythonmusic.midi.message import Message
from pythonmusic.util import assert_range, instrument_get_patch_bank, make_instrument

__all__ = ["Target", "SfTarget", "MidiOutTarget", "EmptyTarget"]


class Target(ABC):
    """
    A type that defines an interface for objects that receive and handle
    midi messages. :obj:`Players <pythonmusic.play.player.Player>` use targets
    to play midi messages.

    Implementations of this class should override methods such as `note_on`,
    `note_off`, ... and replace with their desired behaviour.
    """

    def midi_message(self, message: Message) -> bool:
        """
        Interprets and parses the given midi message, and calls the method
        associated with the message's type.

        By default, this method only handles a small set of common midi message
        types:

        * note on
        * note off
        * after touch
        * control change
        * program change
        * channel pressure
        * pitch wheel

        In order to add other message types, you need to override this method
        and check the types manually. This method returns `True` if the message
        was handled, so you do not need to reimplement handling of the events
        above:

        .. code-block:: python

            ...
            @override
            def midi_message(self, message: Message) -> bool:
                if super().midi_message(self, message):
                    return True

                match message.type():
                    ...

        Args:
            message(Message): A midi message

        Returns:
            bool: `True` if the message was handled
        """

        match message.type():
            case mm.NOTE_OFF:
                self.note_off(message.channel, message.key, message.velocity)
            case mm.NOTE_ON:
                # some keyboards send a note off as a zero-velocity note on
                velocity = message.velocity
                if velocity == 0:
                    self.note_off(message.channel, message.key, 0)
                else:
                    self.note_on(message.channel, message.key, velocity)
            case mm.AFTERTOUCH:
                self.aftertouch(message.channel, message.key, message.pressure)
            case mm.CONTROL_CHANGE:
                self.control_change(message.channel, message.control, message.value)
            case mm.PROGRAM_CHANGE:
                self.program_change(message.channel, message.program)
            case mm.CHANNEL_PRESSURE:
                self.channel_pressure(message.channel, message.pressure)
            case mm.PITCH_WHEEL:
                self.pitch_bend(message.channel, message.pitch_bend)
            case _:
                return False

        return True

    def note_off(self, channel: int, key: int, velocity: int):
        """
        Sends a note off event.

        When implementing this method yourself, you may want to still call
        `super().note_off()`. Internally, targets keep track of which notes they
        play, so that, should the target be deleted before all notes stop playing,
        it can send note off events to connected devices.

        Args:
            channel(int): The note's channel
            key(int): The note's key/pitch
            velocity(int): The note's velocity
        """
        del channel
        del key
        del velocity

    def note_on(self, channel: int, key: int, velocity: int):
        """
        Sends a note on event.

        When implementing this method yourself, you may want to still call
        `super().note_on()`. Internally, targets keep track of which notes they
        play, so that, should the target be deleted before all notes stop playing,
        it can send note off events to connected devices.

        Args:
            channel(int): The note's channel
            key(int): The note's key/pitch
            velocity(int): The note's velocity
        """
        del channel
        del key
        del velocity

    def aftertouch(self, channel: int, key: int, value: int):
        """
        Sends an aftertouch event.

        Args:
            channel(int): The event's channel
            key(int): The event's key
            value(int): The aftertouch value
        """
        del channel
        del key
        del value

    def control_change(self, channel: int, control: int, value: int):
        """
        Sends a control change event.

        Args:
            channel(int): The cc's channel
            control(int): The cc id
            value(int): The cc's value
        """
        del channel
        del control
        del value

    def program_change(self, channel: int, program: int):
        """
        Sends a program change event.

        Args:
            channel(int): The program change's channel
            program(int): The change's program
        """
        del channel
        del program

    def channel_pressure(self, channel: int, value: int):
        """
        Sends a channel pressure event.

        Args:
            channel(int): The event's channel
            value(int): The event's pressure
        """
        del channel
        del value

    def pitch_bend(self, channel: int, value: int):
        """
        Sends a pitch bend event.

        Args:
            channel(int): The change's channel
            value(int): The pitch value
        """
        del channel
        del value

    def set_instrument(self, channel: int, instrument: int):
        """
        Updates the target's instrument.

        The given instrument must be defined in this library's instrument
        constants.

        Args:
            channel(int): The channel for which to change the instrument
            instrument(int): The new instrument.
        """

        patch, bank = instrument_get_patch_bank(instrument)
        self.midi_message(Message.new_program_change(channel, patch))
        self.midi_message(Message.new_control_change(channel, BANK_CHANGE, bank))


class EmptyTarget(Target):
    """
    A target implementation that does nothing. Use this class if you need a
    dummy target or to mute playback for classes that require a target.
    """

    pass


class SfTarget(Target):
    """
    A target implementation that allows playback of midi messages via a sound
    font.

    Sound fonts differ in their base volume. If your playback is too loud or too
    quiet, you can adjust the font's base level with the `gain` parameter. All
    values between `-3` (quieter) and `3` (louder) are valid.

    Args:
        sound_font(str): Path to a sound font
        gain(int): Gain from `-3` to `3`
    """

    def __init__(self, sound_font: str, gain: int = 0):
        assert_range(gain, -3, 3)

        # for now, this will only support one sound font at a time
        super().__init__()

        self._target = TsfSynth()
        self._sfid = self._target.sfload(abspath(expanduser(sound_font)), gain)
        self._target.start()

        self._target.program_change(PERCUSSION_CHANNEL, 127, True)

    def __del__(self):
        # aims to prevent an error message on macOS
        self._target.stop()
        del self._target

    @override
    def note_on(self, channel: int, key: int, velocity: int):
        """:meta private:"""
        super().note_on(channel, key, velocity)
        self._target.noteon(channel, key, velocity)

    @override
    def note_off(self, channel: int, key: int, velocity: int):
        """:meta private:"""
        super().note_off(channel, key, velocity)
        self._target.noteoff(channel, key)

    @override
    def control_change(self, channel: int, control: int, value: int):
        """:meta private:"""
        super().control_change(channel, control, value)
        self._target.control_change(channel, control, value)

    @override
    def program_change(self, channel: int, program: int):
        """:meta private:"""
        super().program_change(channel, program)
        self._target.program_change(channel, program, channel == PERCUSSION_CHANNEL)

    @override
    def pitch_bend(self, channel: int, value: int):
        """:meta private:"""
        super().pitch_bend(channel, value)
        # midi uses two bytes (7 bit available) to represent pitch bend
        # this library uses only the msb (0..128), so we need to shift
        self._target.pitchbend(channel, value << 7)

    def pitch_range(self, channel: int, semitones: float):
        """
        Sets the pitch bend range in semitones for the given channel.

        Args:
            channel(int): The channel for which to change the range
            semitones(float): New range in semitones
        """
        self._target.pitchbend_range(channel, semitones)

    def instrument(self, channel: int) -> int:
        """
        Returns the currently selected instrument on the given channel.

        The returned instrument is build from the internal patch and bank.

        Args:
            channel(int): The channel to check

        Returns:
            int: The current instrument
        """
        info = self._target.program_info(channel)
        return make_instrument(info[2], info[1])

    def reset_instruments(self):
        """
        Sets instruments on all channels to patch/program 0, bank 0.
        """
        for channel in range(16):
            self.set_instrument(channel, ACOUSTIC_GRAND_PIANO)

    def notes_off(self, channel: Optional[int] = None):
        """
        Turns all notes off on the given channel. If `channel` is `None`,
        applies to all channels.

        This only signalls to the target that currently playing notes should be
        stopped. To stop all sound, use `sounds_off()`.

        Args:
            channel(Optional[int]): Channel to apply to, or all channels if `None`
        """
        self._target.notes_off(channel)

    def sounds_off(self, channel: Optional[int]):
        """
        Stopps all sounds on the given channel.

        Args:
            channel(Optional[int]): Channel to apply to, or all channels if `None`
        """
        self._target.sounds_off(channel)


class MidiOutTarget(Target):
    """
    A target implementation for sending midi messages to midi input ports.

    For more information, see :obj:`MidiOut <pythonmusic.midi.MidiOut>`.

    Args:
        name(str): Name of midi device or virtual port
        virtual(bool): If `True` opens a new port, or attaches to an open input
            port if `False`.
    """

    def __init__(self, name: str, virtual: bool):
        self._port = MidiOut(name, virtual)

    def __del__(self):
        for channel in range(16):
            self._port.send_message(Message.new_all_notes_off(channel, 0))

    def port(self) -> MidiOut:
        """Returns the internal midi port."""
        return self._port

    @override
    def midi_message(self, message: Message) -> bool:
        """
        Sends the given midi message to the internal midi port.

        Unlike other target implementations, this message forwards to the the
        `MidiOut` instance directly. Handler methods are not called.

        :meta private:

        Args:
            message(Message): A midi message

        Returns:
            bool: `True` if the message was handled
        """
        self._port.send_message(message)
        return True
