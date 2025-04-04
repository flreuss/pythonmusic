from struct import Struct
from typing import Self

import pythonmusic.constants.messages as _messages
from pythonmusic.constants.meta import (
    META_COPYRIGHT_NOTICE,
    META_END_OF_TRACK,
    META_INSTRUMENT_NAME,
    META_SEQUENCE_NUMBER,
    META_SET_TEMPO,
    META_TEXT,
    META_TRACK_NAME,
)
from pythonmusic.util import assert_range, int_to_vlq

__all__ = ["InvalidMessageError", "Message"]


class InvalidMessageError(Exception):
    """
    An error that is raised if data is read from an invalid message.
    """

    pass


# TODO: docs


# time in ms from start
class Message:
    """
    A midi message.
    """

    # time is midi ticks

    __slots__ = ("data", "time")

    def __init__(self, data: bytearray | bytes | list[int], time: int = 0) -> None:
        self.data: bytearray = bytearray(data)
        self.time: int = time

    # properties
    def __eq__(self, other: object, /) -> bool:
        if type(other) != Message:
            return False

        if self.raw() == other.raw() and self.time == other.time:
            return True

        return False

    def __lt__(self, other: Self) -> bool:
        return self.time < other.time

    def __len__(self) -> int:
        # returns length of message
        return len(self.data)

    def __str__(self) -> str:
        return self.description()

    def __repr__(self) -> str:
        return f"({list(self.data)}, {self.time})"

    def description(self) -> str:
        """Returns a full description of the message."""
        out = "Message("
        match self.type():
            case _messages.NOTE_ON:
                out += f'"note_on", channel: {self.channel}, key: {self.key}, velocity: {self.velocity}'
            case _messages.NOTE_OFF:
                out += f'"note_off", channel: {self.channel}, key: {self.key}, velocity: {self.velocity}'
            case _messages.AFTERTOUCH:
                out += f'"aftertouch", channel: {self.channel}, key: {self.key}, pressure: {self.pressure}'
            case _messages.CONTROL_CHANGE:
                out += f'"control_change", channel: {self.channel}, control: {self.control}, value: {self.value}'
            case _messages.PROGRAM_CHANGE:
                out += f'"program_change", channel: {self.channel}, program: {self.program}'
            case _messages.CHANNEL_PRESSURE:
                out += f'"channel_pressure", channel: {self.channel}, pressure: {self.pressure}'
            case _messages.PITCH_WHEEL:
                out += (
                    f'"pitch_bend", channel: {self.channel}, value: {self.pitch_bend}'
                )
            case _messages.SYSTEM_EXCLUSIVE:
                out += '"system_exclusive"'
            case _messages.TIME_CODE_QF:
                out += '"time_code_qf"'
            case _messages.SONG_SELECT:
                out += '"song_select"'
            case _messages.SONG_POSITION:
                out += '"song_position"'
            case _messages.TUNE_REQUEST:
                out += '"tune_request"'
            case _messages.CLOCK:
                out += '"clock"'
            case _messages.START:
                out += '"start"'
            case _messages.CONTINUE:
                out += '"continue"'
            case _messages.STOP:
                out += '"stop"'
            case _messages.ACTIVE_SENSING:
                out += '"active_sensing"'
            case _messages.RESET:
                out += '"reset"'
            case _messages.META:
                out += '"meta'
            case _:
                out += f'"other"'

        out += f", time: {self.time})"

        return out

    def is_empty(self) -> bool:
        """
        Returns `True` if the message does not contain data.
        """
        return self.__len__() == 0

    # message type
    def is_meta(self) -> bool:
        """
        Returns `True` if this message is a meta message.

        Does not raise an exeption on empty message, instead returns `False`.
        """
        # meta messages are identified by an initial 0xFF in their first byte
        if self.is_empty():
            return False

        return self.data[0] == 0xFF

    def raw(self) -> bytes:
        """
        Returns the raw data from the message.
        """
        return bytes(self.data)

    def raw_with_time(self) -> bytes:
        """
        Returns with raw data of this message prefixed by its delta time in
        vlq format.
        """
        return int_to_vlq(self.time) + self.raw()

    # will remain function, because it's not mutable
    def type(self) -> int:
        """
        Returns the type of the message.

        If the message header contains a channel, it is removed. The resulting
        value will be the four remaining bits from the header, which can be
        checked against the defined constants. If the entire header is used to
        identify the message type, the whole header is returned.

        Keep in mind that the interpretation of a midi message may change
        depending on its context: meta messages (0xFF) must not be streamed to a
        MIDI device.

        Returns:
            int: The type of the message

        Raises:
            InvalidMessageError: If the message is ill-formed
        """

        if self.is_empty():
            raise InvalidMessageError

        raw = self.data[0]
        if raw >= 0b11110000:
            return raw
        else:
            return raw >> 4

    # properties
    def _assert_non_empty(self):
        if self.is_empty():
            raise InvalidMessageError("Empty message")

    def _assert_channel(self):
        if (self.data[0] >> 4) >= 0b1111:
            raise AttributeError("message type does not store channel")

    def _assert_key(self):
        if (self.data[0] >> 4) > 0b1010:
            raise AttributeError("message type does not store key")

    def _assert_control(self):
        if (self.data[0] >> 4) != _messages.CONTROL_CHANGE:
            raise AttributeError("message type does not store control")

    def _assert_value(self):
        if (self.data[0] >> 4) >= 0b1111:
            raise AttributeError("message type does not store value")

    def _assert_velocity(self):
        if (self.data[0] >> 4) > 0b1001:
            raise AttributeError("message type does not store velocity")

    def _assert_pressure(self):
        t = self.type()
        if t != _messages.AFTERTOUCH and t != _messages.CHANNEL_PRESSURE:
            raise AttributeError("message type does not store pressure")

    def _assert_program(self):
        if (self.data[0] >> 4) != _messages.PROGRAM_CHANGE:
            raise AttributeError("message type does not store program")

    def _assert_pitch_bend(self):
        if (self.data[0] >> 4) != _messages.PITCH_WHEEL:
            raise AttributeError("message type does not store pitch value")

    @property
    def channel(self) -> int:
        """The channel of the message."""
        self._assert_non_empty()
        self._assert_channel()
        return self.data[0] & 0b00001111

    @channel.setter
    def channel(self, new_value: int):
        assert_range(new_value, 0, 15)
        self._assert_non_empty()
        self._assert_channel()

        self.data[0] &= 0b11110000
        self.data[0] |= new_value

    @property
    def key(self) -> int:
        """The key or pitch value of the message."""
        self._assert_non_empty()
        self._assert_key()
        return self.data[1]

    @key.setter
    def key(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._assert_non_empty()
        self._assert_key()

        self.data[1] = new_value

    @property
    def control(self) -> int:
        """The control value of the message."""
        self._assert_non_empty()
        self._assert_control()
        return self.data[1]

    @control.setter
    def control(self, new_value: int):
        self._assert_non_empty()
        self._assert_control()
        self.data[1] = new_value

    @property
    def value(self) -> int:
        """
        Returns the value parameter of the midi message.

        The value parameter generally refers to the last byte of the midi
        message. For note on/off events, this is velocity, for control changes,
        the control value.

        This property does not cover system common and system real-time messages.
        """
        self._assert_non_empty()
        self._assert_value()

        t = self.type()
        if t == _messages.PROGRAM_CHANGE or t == _messages.CHANNEL_PRESSURE:
            return self.data[1]
        else:
            # this also includes pitch wheel (only the msb are used)
            return self.data[2]

    @value.setter
    def value(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._assert_non_empty()
        self._assert_value()

        t = self.type()
        if t == _messages.PROGRAM_CHANGE or t == _messages.CHANNEL_PRESSURE:
            self.data[1] = new_value
        else:
            self.data[2] = new_value
            # this library doesn't use the precise PB byte; set it to 0, if
            # updated
            if t == _messages.PITCH_WHEEL:
                self.data[1] = 0

    @property
    def velocity(self) -> int:
        """The velocity value of the message."""
        self._assert_non_empty()
        self._assert_velocity()
        return self.data[2]

    @velocity.setter
    def velocity(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._assert_non_empty()
        self._assert_velocity()
        self.data[2] = new_value

    @property
    def pressure(self) -> int:
        """The pressure value of the message."""
        self._assert_non_empty()
        self._assert_pressure()
        if self.type() == _messages.AFTERTOUCH:
            return self.data[2]
        else:
            return self.data[1]

    @pressure.setter
    def pressure(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._assert_non_empty()
        self._assert_pressure()
        if self.type() == _messages.AFTERTOUCH:
            self.data[2] = new_value
        else:
            self.data[1] = new_value

    @property
    def program(self) -> int:
        """The program value of the message."""
        self._assert_non_empty()
        self._assert_program()
        return self.data[1]

    @program.setter
    def program(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._assert_non_empty()
        self._assert_program()
        self.data[1] = new_value

    @property
    def pitch_bend(self) -> int:
        """The pitch bend value of the message."""
        self._assert_non_empty()
        self._assert_pitch_bend()
        return self.data[2]

    @pitch_bend.setter
    def pitch_bend(self, new_value: int):
        assert_range(new_value, 0, 127)
        self._assert_non_empty()
        self._assert_pitch_bend()
        # library uses less-precise PB resolution
        self.data[1] = 0
        self.data[2] = new_value

    # type inits
    @classmethod
    def new_note_on(cls, channel: int, key: int, velocity: int, time: int = 0) -> Self:
        """
        Creates a new note on message.

        Args:
            channel(int): The channel of the message
            key(int): The key of the message
            velocity(int): The velocity of the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        assert_range(channel, 0, 15)
        assert_range(key, 0, 127)
        assert_range(velocity, 0, 127)

        header = (_messages.NOTE_ON << 4) | channel
        message_bytes = bytearray([header, key, velocity])
        return cls(message_bytes, time)

    @classmethod
    def new_note_off(cls, channel: int, key: int, velocity: int, time: int = 0) -> Self:
        """
        Creates a new note off message.

        Args:
            channel(int): The channel of the message
            key(int): The key of the message
            velocity(int): The velocity of the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        assert_range(channel, 0, 15)
        assert_range(key, 0, 127)
        assert_range(velocity, 0, 127)

        header = (_messages.NOTE_OFF << 4) | channel
        message_bytes = bytearray([header, key, velocity])
        return cls(message_bytes, time)

    @classmethod
    def new_aftertouch(
        cls, channel: int, key: int, pressure: int, time: int = 0
    ) -> Self:
        """
        Creates a new aftertouch message.

        Args:
            channel(int): The channel of the message
            key(int): The key of the message
            pressure(int): The pressure of the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        assert_range(channel, 0, 15)
        assert_range(key, 0, 127)
        assert_range(pressure, 0, 127)

        header = (_messages.AFTERTOUCH << 4) | channel
        message_bytes = bytearray([header, key, pressure])
        return cls(message_bytes, time)

    @classmethod
    def new_control_change(
        cls, channel: int, control: int, value: int, time: int = 0
    ) -> Self:
        """
        Creates a new control change message.

        The given control must be `119` or below. `120` to `127` are reserved
        for channel mode messages.

        Args:
            channel(int): The channel for which to change the control
            control(int): The control of the message
            value(int): The control value of the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        assert_range(channel, 0, 15)
        # controls 120 - 127 are reserved for channel mode messages
        # they available below
        assert_range(control, 0, 119)
        assert_range(value, 0, 127)

        header = (_messages.CONTROL_CHANGE << 4) | channel
        message_bytes = bytearray([header, control, value])
        return cls(message_bytes, time)

    @classmethod
    def new_program_change(cls, channel: int, program: int, time: int = 0) -> Self:
        """
        Creates a new program change message.

        Args:
            channel(int): The channel for which to change the program
            program(int): The program value of the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """

        assert_range(channel, 0, 15)
        assert_range(program, 0, 127)

        header = (_messages.PROGRAM_CHANGE << 4) | channel
        message_bytes = bytearray([header, program])
        return cls(message_bytes, time)

    @classmethod
    def new_channel_pressure(cls, channel: int, pressure: int, time: int = 0) -> Self:
        """
        Creates a new channel pressure message.

        Args:
            channel(int): The channel for which to change pressure
            pressure(int): The pressure value of the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """

        assert_range(channel, 0, 15)
        assert_range(pressure, 0, 127)

        header = (_messages.CHANNEL_PRESSURE << 4) | channel
        message_bytes = bytearray([header, pressure])
        return cls(message_bytes, time)

    @classmethod
    def new_pitch_bend(cls, channel: int, value: int, time: int = 0) -> Self:
        """
        Creates a new pitch bend message.

        This library only uses the msb for pitch bend representation. The more
        precise bits are ignored.

        Args:
            channel(int): The channel for which to change pitch bend for
            value(int): The new value of the pitch bend
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """

        assert_range(channel, 0, 15)
        assert_range(value, 0, 127)

        header = (_messages.PITCH_WHEEL << 4) | channel
        message_bytes = bytearray([header, 0, value])
        return cls(message_bytes, time)

    @classmethod
    def _new_channel_mode(
        cls, channel: int, control: int, value: int, time: int
    ) -> Self:
        assert_range(channel, 0, 15)
        assert_range(control, 120, 127)
        assert_range(value, 0, 127)

        header = (_messages.CHANNEL_MODE << 4) | channel
        message_bytes = bytearray([header, control, value])
        return cls(message_bytes, time)

    @classmethod
    def new_sound_off(cls, channel: int, time: int = 0) -> Self:
        """
        Creates a new sound off message.

        Args:
            channel(int): The channel for which to send the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 120, 0, time)

    @classmethod
    def new_reset_controllers(cls, channel: int, time: int = 0) -> Self:
        """
        Creates a new reset controlers message.

        Args:
            channel(int): The channel for which to send the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 121, 0, time)

    @classmethod
    def new_local_control(cls, channel: int, state: bool, time: int = 0) -> Self:
        """
        Creates a new local control message.

        Args:
            channel(int): The channel for which to send the message
            state(bool): If `True`, enables local control, disables otherwise
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 122, 127 if state else 0, time)

    @classmethod
    def new_all_notes_off(cls, channel: int, time: int = 0) -> Self:
        """
        Creates a new all notes off message.

        Args:
            channel(int): The channel for which to send the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 123, 0, time)

    @classmethod
    def new_omni_mode(cls, channel: int, state: bool, time: int = 0) -> Self:
        """
        Creates a new omni mode message.

        Args:
            channel(int): The channel for which to send the message
            state(bool): `True` to enable omni mode, `False` to disable
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 125 if state else 124, 0, time)

    @classmethod
    def new_mono_mode(cls, channel: int, number: int, time: int = 0) -> Self:
        """
        Creates a new mono mode message.

        Args:
            channel(int): The channel for which to send the message
            number(int): Number of channels to use, `0` to disable
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 126, number, time)

    @classmethod
    def new_poly_mode(cls, channel: int, time: int = 0) -> Self:
        """
        Creates a new poly mode message.

        Args:
            channel(int): The channel for which to send the message
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls._new_channel_mode(channel, 127, 0, time)

    @classmethod
    def new_system_exclusive(
        cls, manufacturer: list[int], data: list[int], time: int = 0
    ) -> Self:
        """
        Creates a new system excludive message.

        When adding your data, you do not need to include the termination byte.

        Args:
            manufacturer(list[int]): Byte identifier for manufacturer
            data(list[int]): Data bytes
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        # manufacturer id needs to be one or three bytes
        assert len(manufacturer) == 1 or len(manufacturer) == 3
        # and msb of each byte needs to be 0
        for byte in manufacturer:
            assert byte <= 127

        # msb in data's bytes must be 0
        for byte in data:
            assert byte <= 127

        raw: list[int] = []
        raw.append(_messages.SYSTEM_EXCLUSIVE)
        raw.extend(manufacturer)
        raw.extend(data)
        raw.append(_messages.END_OF_SYSTEM_EXCLUSIVE)

        message_bytes = bytearray(raw)
        return cls(message_bytes, time)

    @classmethod
    def new_time_code_qf(cls, type: int, values: int, time: int = 0) -> Self:
        """
        Creates a new time code quarter frame message.

        Args:
            type(int): Message type
            values(int): Values
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        assert_range(type, 0, 7)
        assert_range(type, 0, 15)

        payload = (type << 4) | values
        message_bytes = bytearray([_messages.TIME_CODE_QF, payload])
        return cls(message_bytes, time)

    @classmethod
    def new_song_select(cls, song: int, time: int = 0) -> Self:
        """
        Creates a new song select message.

        Args:
            song(int): Song number to select
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        assert_range(song, 0, 127)

        message_bytes = bytearray([_messages.SONG_SELECT, song])
        return cls(message_bytes, time)

    @classmethod
    def new_tune_request(cls, time: int = 0) -> Self:
        """
        Creates a new tune request message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.TUNE_REQUEST]), time)

    @classmethod
    def new_clock(cls, time: int = 0) -> Self:
        """
        Creates a new clock message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.CLOCK]), time)

    @classmethod
    def new_start(cls, time: int = 0) -> Self:
        """
        Creates a new start message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.START]), time)

    @classmethod
    def new_continue_song(cls, time: int = 0) -> Self:
        """
        Creates a new continue song message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.CONTINUE]), time)

    @classmethod
    def new_stop(cls, time: int = 0) -> Self:
        """
        Creates a new stop message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.STOP]), time)

    @classmethod
    def new_active_sensing(cls, time: int = 0) -> Self:
        """
        Creates a new active sensing message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.ACTIVE_SENSING]), time)

    @classmethod
    def new_reset(cls, time: int = 0) -> Self:
        """
        Creates a new rest message.

        Args:
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi message
        """
        return cls(bytearray([_messages.RESET]), time)

    @classmethod
    def new_meta(cls, type: int, data: bytes, time: int = 0) -> Self:
        """
        Creates a new meta message.

        The data length byte is added automatically.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            data(bytearray): The data of the message.
            time(int): Time offset in ticks from last message

        Returns:
            Message: A new midi meta message
        """
        assert_range(type, 0, 255)

        message_bytes: bytearray = bytearray()
        message_bytes.append(_messages.META)
        message_bytes.append(type)
        message_bytes.append(len(data))  # yes, this breaks if data > 127
        message_bytes.extend(data)
        return cls(message_bytes, time)

    @classmethod
    def new_meta_sequence_number(cls, n: int) -> Self:
        """
        Creates a new sequence number meta message.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            n(int): A 16-bit integer (up to 65535)

        Returns: A new midi meta message
        """
        assert_range(n, 0, 0xFFFF)
        return cls.new_meta(META_SEQUENCE_NUMBER, Struct(">I").pack(n))

    @classmethod
    def _meta_text_base(cls, text: str, type: int, time: int) -> Self:
        text_ascii = ascii(text).encode("ascii")
        if len(text_ascii) > 0xFF:
            raise ValueError(
                'Text must not exceede 255 characters, "f{name_ascii}" contains f{name_len}'
            )
        return cls.new_meta(type, text_ascii, time)

    @classmethod
    def new_meta_text(cls, text: str, time: int = 0) -> Self:
        """
        Creates a new text meta message.

        The provided text is converted to ASCII and cannot be longer than
        `255` characters.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            text(str): A string
            time(int): The time offset in ticks

        Returns:
            A new meta message
        """
        return cls._meta_text_base(text, META_TEXT, time)

    @classmethod
    def new_meta_copyright(cls, copyright: str) -> Self:
        """
        Creates a new copyright meta message.

        The provided copyright must is converted to ASCII and cannot be longer
        than `255` characters.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            copyright(str): The copyright string

        Returns:
            Message: A new midi meta message
        """
        return cls._meta_text_base(copyright, META_COPYRIGHT_NOTICE, 0)

    @classmethod
    def new_meta_track_name(cls, track_name: str) -> Self:
        """
        Creates a new track name meta message.

        The provided track name must be representable in ASCII and cannot
        be longer `255` characters.

        As per specification, the `time` attribute is always `0`.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            track_name(str): The name of the track.

        Returns:
            Message: A new midi meta message
        """
        return cls._meta_text_base(track_name, META_TRACK_NAME, 0)

    @classmethod
    def new_meta_instrument_name(cls, instrument_name: str, time: int = 0) -> Self:
        """
        Creates a new instrument name meta message.

        The provided instrument name must be representable in ASCII and cannot
        be longer `255` characters.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            instrument_name(str): Name of the instrument
            time(int): Time offset in ticks

        Returns:
            Message: A new midi meta message
        """
        return cls._meta_text_base(instrument_name, META_INSTRUMENT_NAME, time)

    @classmethod
    def new_meta_end_of_track(cls, time: int = 0) -> Self:
        """
        Creates a new end of track midi meta message.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            time(int): The time offset in ticks

        Returns:
            Message: A new midi meta message
        """
        return cls.new_meta(META_END_OF_TRACK, bytes(), time)

    @classmethod
    def new_meta_tempo(cls, tempo: int, time: int = 0) -> Self:
        """
        Creates a new set tempo midi meta message.

        .. important :: Meta messages may exist in midi files, but must not be
            sent to midi ports or devices.

        Args:
            tempo(int): Tempo in microseconds per quarter note.
            time(int): The time offset in ticks

        Returns:
            Message: A new midi meta message
        """
        assert_range(tempo, 1, 16777215)
        return cls.new_meta(META_SET_TEMPO, tempo.to_bytes(3, "big"), time)
