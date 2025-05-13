META_SEQUENCE_NUMBER: int = 0x00
"""
Meta message type id for a sequence number.
"""

META_TEXT: int = 0x01
"""
Meta message type id for text.
"""

META_COPYRIGHT_NOTICE: int = 0x02
"""
Meta message type id for a copyright notice.
"""

META_TRACK_NAME: int = 0x03
"""
Meta message type id for a track name.
"""

META_INSTRUMENT_NAME: int = 0x04
"""
Meta message type id for an instrument name.
"""

META_LYRICS: int = 0x05
"""
Meta message type id for a lyrics entry.

Lyrics are usually represented by a syllable per quarter note.
"""

META_MARKER: int = 0x06
"""
Meta message type id for a marker.
"""

META_CUE_POINT: int = 0x07
"""
Meta message type id for a cue point.
"""

META_CHANNEL_PREFIX: int = 0x20
"""
Meta message type id for a channel prefix.
"""

META_END_OF_TRACK: int = 0x2F
"""
Meta message type id for an end of track message.
"""

META_SET_TEMPO: int = 0x51
"""
Meta message type id for set tempo.
"""

META_SMPTE_OFFSET: int = 0x54
"""
Meta message type id for an SMPTE offset.
"""

META_TIME_SIGNATURE: int = 0x58
"""
Meta message type id for a time signature.
"""

META_KEY_SIGNATURE: int = 0x59
"""
Meta message type id for a key signature.
"""
