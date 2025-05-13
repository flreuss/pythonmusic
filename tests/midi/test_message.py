import unittest

from pythonmusic.constants import *
from pythonmusic.midi.message import Message


class MessageTests(unittest.TestCase):
    def test_init(self):
        header = (NOTE_ON << 4) | 2
        pitch = 60
        velocity = 120
        time = 123
        m_bytes = bytearray([header, pitch, velocity])
        m = Message(m_bytes, time)

        self.assertFalse(m.is_meta())
        self.assertFalse(m.is_empty())
        self.assertEqual(m.type(), NOTE_ON)

        self.assertEqual(m.key, pitch)
        self.assertEqual(m.velocity, velocity)
        self.assertEqual(m.value, velocity)
        self.assertEqual(m.time, time)

        n = Message([header, pitch, velocity], time)
        self.assertEqual(m, n)

        o = Message([], 0)
        self.assertEqual(len(o), 0)

    def test_len(self):
        m = Message(bytearray([(NOTE_OFF << 4) | 2, 23, 23]), 0)
        self.assertEqual(len(m), 3)
        m = Message.new_system_exclusive([34], [2, 4, 127], 34)
        self.assertEqual(len(m), 6)

    def test_str(self):
        m = Message.new_note_on(0, 60, 100)
        self.assertEqual(
            str(m), 'Message("note_on", channel: 0, key: 60, velocity: 100, time: 0)'
        )

        m = Message.new_note_off(0, 60, 100)
        self.assertEqual(
            str(m), 'Message("note_off", channel: 0, key: 60, velocity: 100, time: 0)'
        )

        m = Message.new_reset()
        self.assertEqual(str(m), 'Message("reset", time: 0)')

    # description is same as above

    def test_is_empty(self):
        self.assertTrue(Message([], 0).is_empty())
        self.assertFalse(Message.new_note_on(0, 10, 10, 0).is_empty())

    def test_is_meta(self):
        self.assertTrue(Message.new_meta(0x2F, bytes(), 0).is_meta())
        self.assertFalse(Message.new_note_on(0, 10, 10, 0).is_meta())

    def test_raw(self):
        self.assertEqual(
            Message.new_note_on(0, 4, 34, 0).raw(), bytes([0b10010000 | 0, 4, 34])
        )
        self.assertEqual(
            Message.new_meta_tempo(500000, 0).raw(),
            bytes([0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20]),
        )

    def test_raw_with_time(self):
        self.assertEqual(
            Message.new_note_on(0, 4, 34, 0).raw_with_time(),
            bytes([0x00, 0b10010000 | 0, 4, 34]),
        )
        self.assertEqual(
            Message.new_meta_tempo(500000, 30).raw_with_time(),
            bytes([30, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20]),
        )
        self.assertEqual(
            Message.new_meta_tempo(500000, 0b10_0000001).raw_with_time(),
            bytes([0b10000010, 0b00000001, 0xFF, 0x51, 0x03, 0x07, 0xA1, 0x20]),
        )

    def test_type(self):
        self.assertEqual(Message.new_note_on(0, 10, 10, 0).type(), NOTE_ON)
        self.assertEqual(Message.new_note_off(0, 10, 10, 0).type(), NOTE_OFF)
        self.assertEqual(Message.new_aftertouch(0, 0, 0, 0).type(), AFTERTOUCH)
        self.assertEqual(Message.new_meta(0x2F, bytes(), 0).type(), META)

    def test_note_on_message(self):
        channel = 5
        key = C4
        velocity = MF
        m = Message.new_note_on(channel, key, velocity)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.key, key)
        self.assertEqual(m.velocity, velocity)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), NOTE_ON)

        m.channel = 1
        m.key = D5
        m.velocity = FF

        self.assertEqual(m.channel, 1)
        self.assertEqual(m.key, D5)
        self.assertEqual(m.velocity, FF)

    def test_note_off_message(self):
        channel = 5
        key = C4
        velocity = MF
        m = Message.new_note_off(channel, key, velocity)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.key, key)
        self.assertEqual(m.velocity, velocity)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), NOTE_OFF)

        m.channel = 1
        m.key = D5
        m.velocity = FF

        self.assertEqual(m.channel, 1)
        self.assertEqual(m.key, D5)
        self.assertEqual(m.velocity, FF)

    def test_aftertouch_message(self):
        channel = 2
        key = C5
        pressure = MF
        m = Message.new_aftertouch(channel, key, pressure)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.key, key)
        self.assertEqual(m.pressure, pressure)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), AFTERTOUCH)

        m.channel = 5
        m.key = D5
        m.pressure = FF

        self.assertEqual(m.channel, 5)
        self.assertEqual(m.key, D5)
        self.assertEqual(m.pressure, FF)

    def test_control_change_message(self):
        channel = 2
        control = SUSTAIN_PEDAL
        value = 127
        m = Message.new_control_change(channel, control, value)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.control, control)
        self.assertEqual(m.value, value)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), CONTROL_CHANGE)

        m.channel = 7
        m.control = CHANNEL_PAN
        m.value = 12

        self.assertEqual(m.channel, 7)
        self.assertEqual(m.control, CHANNEL_PAN)
        self.assertEqual(m.value, 12)

    def test_program_change_message(self):
        channel = 4
        program = VIOLIN
        m = Message.new_program_change(channel, program)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.program, program)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), PROGRAM_CHANGE)

        m.channel = 10
        m.program = ACOUSTIC_GRAND_PIANO

        self.assertEqual(m.channel, 10)
        self.assertEqual(m.program, ACOUSTIC_GRAND_PIANO)

    def test_channel_pressure_message(self):
        channel = 3
        pressure = 120
        m = Message.new_channel_pressure(channel, pressure)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.pressure, pressure)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), CHANNEL_PRESSURE)

        m.channel = 11
        m.pressure = 2

        self.assertEqual(m.channel, 11)
        self.assertEqual(m.pressure, 2)

    def test_pitch_bend_message(self):
        channel = 7
        value = 127
        m = Message.new_pitch_bend(channel, value)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.value, value)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.type(), PITCH_WHEEL)

        m.channel = 8
        m.value = 120

        self.assertEqual(m.channel, 8)
        self.assertEqual(m.value, 120)

    def test_new_sound_off_message(self):
        m = Message.new_sound_off(0)
        self.assertEqual(m.channel, 0)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.control, 120)
        self.assertEqual(m.type(), CHANNEL_MODE)

        m.channel += 1
        self.assertEqual(m.channel, 1)

    def test_new_reset_controllers_message(self):
        channel = 7
        m = Message.new_reset_controllers(channel)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.control, 121)
        self.assertEqual(m.type(), CHANNEL_MODE)

        m.channel = 8
        m.value = 89

        self.assertEqual(m.channel, 8)
        self.assertEqual(m.value, 89)

    def test_new_local_control_message(self):
        channel = 7
        m = Message.new_local_control(channel, True)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.value, 127)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.control, 122)
        self.assertEqual(m.type(), CHANNEL_MODE)

        m.channel = 8

        self.assertEqual(m.channel, 8)

        m = Message.new_local_control(channel, False)
        self.assertEqual(m.value, 0)

    def test_all_notes_off_message(self):
        channel = 8
        m = Message.new_all_notes_off(channel)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.control, 123)
        self.assertEqual(m.type(), CHANNEL_MODE)

        m.channel = 8

        self.assertEqual(m.channel, 8)

    def test_omni_mode_message(self):
        channel = 8
        m = Message.new_omni_mode(channel, True)

        self.assertEqual(m.channel, channel)
        self.assertEqual(m.time, 0)
        self.assertEqual(m.control, 125)
        self.assertEqual(m.type(), CHANNEL_MODE)

        m.channel = 8

        self.assertEqual(m.channel, 8)

        m = Message.new_omni_mode(channel, False)
        self.assertEqual(m.control, 124)
