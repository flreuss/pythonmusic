from pythonmusic.util import make_instrument

__all__ = [
    "ACOUSTIC_GRAND_PIANO",
    "WIDE_ACOUSTIC_GRAND",
    "DARK_ACOUSTIC_GRAND",
    "BRIGHT_ACOUSTIC_PIANO",
    "WIDE_BRIGHT_ACOUSTIC",
    "ELECTRIC_GRAND_PIANO",
    "WIDE_ELECTRIC_GRAND",
    "HONKY_TONK_PIANO",
    "WIDE_HONKY_TONK",
    "RHODES_PIANO",
    "DETUNED_ELECTRIC_PIANO_1",
    "ELECTRIC_PIANO_1_VARIATION",
    "ELECTRIC_PIANO_60S",
    "CHORUSED_ELECTRIC_PIANO",
    "DETUNED_ELECTRIC_PIANO_2",
    "ELECTRIC_PIANO_2_VARIATION",
    "ELECTRIC_PIANO_LEGEND",
    "ELECTRIC_PIANO_PHASE",
    "HARPSICHORD",
    "COUPLED_HARPSICHORD",
    "WIDE_HARPSICHORD",
    "OPEN_HARPSICHORD",
    "CLAVINET",
    "PULSE_CLAVINET",
    "ACOUSTIC_GRAND_PIANO",
    "WIDE_ACOUSTIC_GRAND",
    "DARK_ACOUSTIC_GRAND",
    "BRIGHT_ACOUSTIC_PIANO",
    "WIDE_BRIGHT_ACOUSTIC",
    "ELECTRIC_GRAND_PIANO",
    "WIDE_ELECTRIC_GRAND",
    "HONKY_TONK_PIANO",
    "WIDE_HONKY_TONK",
    "RHODES_PIANO",
    "DETUNED_ELECTRIC_PIANO_1",
    "ELECTRIC_PIANO_1_VARIATION",
    "ELECTRIC_PIANO_60S",
    "CHORUSED_ELECTRIC_PIANO",
    "DETUNED_ELECTRIC_PIANO_2",
    "ELECTRIC_PIANO_2_VARIATION",
    "ELECTRIC_PIANO_LEGEND",
    "ELECTRIC_PIANO_PHASE",
    "HARPSICHORD",
    "COUPLED_HARPSICHORD",
    "WIDE_HARPSICHORD",
    "OPEN_HARPSICHORD",
    "CLAVINET",
    "PULSE_CLAVINET",
    "CELESTA",
    "GLOCKENSPIEL",
    "MUSIC_BOX",
    "VIBRAPHONE",
    "WET_VIBRAPHONE",
    "MARIMBA",
    "WIDE_MARIMBA",
    "XYLOPHONE",
    "TUBULAR_BELL",
    "CHURCH_BELL",
    "CARILLON",
    "DULCIMER",
    "DRAWBAR_ORGAN",
    "DETUNED_ORGAN_1",
    "ORGAN_1_60S",
    "ORGAN_4",
    "PERCUSSIVE_B3_ORGAN",
    "DETUNED_ORGAN_2",
    "ORGAN_5",
    "ROCK_ORGAN",
    "CHURCH_ORGAN_1",
    "CHURCH_ORGAN_2",
    "CHURCH_ORGAN_3",
    "REED_ORGAN",
    "PUFF_ORGAN",
    "FRENCH_ACCORDION",
    "ITALIAN_ACCORDION",
    "HARMONICA",
    "BANDONEON",
    "NYLON_STRING_GUITAR",
    "UKULELE",
    "OPEN_NYLON_GUITAR",
    "NYLON_GUITAR_2",
    "STEEL_STRING_GUITAR",
    "GUITAR_12_STRING",
    "MANDOLIN",
    "STEEL__BODY",
    "JAZZ_GUITAR",
    "HAWAIIAN_GUITAR",
    "CLEAN_ELECTRIC_GUITAR",
    "CHORUS_GUITAR",
    "MID_TONE_GUITAR",
    "MUTED_ELECTRIC_GUITAR",
    "FUNK_GUITAR",
    "FUNK_GUITAR_2",
    "JAZZ_MAN",
    "OVERDRIVEN_GUITAR",
    "GUITAR_PINCH",
    "DISTORTION_GUITAR",
    "FEEDBACK_GUITAR",
    "DISTORTION_RTM_GUITAR",
    "GUITAR_HARMONICS",
    "GUITAR_FEEDBACK",
    "ACOUSTIC_BASS",
    "FINGERED_BASS",
    "FINGER_SLAP",
    "PICKED_BASS",
    "FRETLESS_BASS",
    "SLAP_BASS_1",
    "SLAP_BASS_2",
    "SYNTH_BASS_1",
    "SYNTH_BASS_101",
    "SYNTH_BASS_3",
    "CLAVI_BASS",
    "HAMMER",
    "SYNTH_BASS_2",
    "SYNTH_BASS_4",
    "RUBBER_BASS",
    "ATTACK_PULSE",
    "VIOLIN",
    "SLOW_VIOLIN",
    "VIOLA",
    "CELLO",
    "CONTRABASS",
    "TREMOLO_STRINGS",
    "PIZZICATO_STRINGS",
    "HARP",
    "YANG_QIN",
    "TIMPANI",
    "STRING_ENSEMBLE",
    "ORCHESTRA_STRINGS",
    "STRINGS_60S",
    "SLOW_STRING_ENSEMBLE",
    "SYNTH_STRINGS_1",
    "SYNTH_STRINGS_3",
    "SYNTH_STRINGS_2",
    "CHOIR_AAHS",
    "CHOIR_AAHS_2",
    "VOICE_OOHS",
    "HUMMING",
    "SYNTH_VOICE",
    "ANALOG_VOICE",
    "ORCHESTRA_HIT",
    "BASS_HIT",
    "HIT_6TH",
    "EURO_HIT",
    "TRUMPET",
    "DARK_TRUMPET",
    "TROMBONE",
    "TROMBONE_2",
    "BRIGHT_TROMBONE",
    "TUBA",
    "MUTED_TRUMPET",
    "MUTED_TRUMPET_2",
    "FRENCH_HORNS",
    "FRENCH_HORN_2",
    "BRASS_SECTION_1",
    "BRASS_SECTION_2",
    "SYNTH_BRASS_1",
    "SYNTH_BRASS_3",
    "ANALOG_BRASS_1",
    "JUMP_BRASS",
    "SYNTH_BRASS_2",
    "SYNTH_BRASS_4",
    "ANALOG_BRASS_2",
    "SOPRANO_SAX",
    "ALTO_SAX",
    "TENOR_SAX",
    "BARITONE_SAX",
    "OBOE",
    "ENGLISH_HORN",
    "BASSOON",
    "CLARINET",
    "PICCOLO",
    "FLUTE",
    "RECORDER",
    "PAN_FLUTE",
    "BOTTLE_BLOW",
    "SHAKUHACHI",
    "WHISTLE",
    "OCARINA",
    "SQUARE_LEAD",
    "SQUARE_WAVE",
    "SINE_WAVE",
    "SAW_LEAD",
    "SAW_WAVE",
    "DOCTOR_SOLO",
    "NATURAL_LEAD",
    "SEQUENCED_SAW",
    "SYNTH_CALLIOPE",
    "CHIFFER_LEAD",
    "CHARANG",
    "WIRE_LEAD",
    "SOLO_SYNTH_VOX",
    "SAW_WAVE_5TH",
    "BASS__LEAD",
    "DELAYED_LEAD",
    "ICE_RAIN",
    "SOUNDTRACK",
    "CRYSTAL",
    "SYNTH_MALLET",
    "ATMOSPHERE",
    "BRIGHTNESS",
    "GOBLIN",
    "ECHO_DROPS",
    "ECHO_BELL",
    "ECHO_PAN",
    "STAR_THEME",
    "SITAR",
    "SITAR_2",
    "BANJO",
    "SHAMISEN",
    "KOTO",
    "TAISHO_KOTO",
    "KALIMBA",
    "BAGPIPE",
    "FIDDLE",
    "SHANAI",
    "TINKLE_BELL",
    "AGOGO",
    "STEEL_DRUMS",
    "WOODBLOCK",
    "CASTANETS",
    "TAIKO",
    "CONCERT_BASS_DRUM",
    "MELODIC_TOM_1",
    "MELODIC_TOM_2",
    "SYNTH_DRUM",
    "TOM_808",
    "ELECTRIC_PERCUSSION",
    "REVERSE_CYMBAL",
    "GUITAR_FRET_NOISE",
    "GUITAR_CUT_NOISE",
    "STRING_SLAP",
    "BREATH_NOISE",
    "FLUTE_KEY_CLICK",
    "SEASHORE",
    "RAIN",
    "THUNDER",
    "WIND",
    "STREAM",
    "BUBBLE",
    "BIRD",
    "DOG",
    "HORSE_GALLOP",
    "BIRD_2",
    "TELEPHONE_1",
    "TELEPHONE_2",
    "DOOR_CREAKING",
    "DOOR_CLOSING",
    "SCRATCH",
    "WIND_CHIMES",
    "HELICOPTER",
    "CAR_ENGINE",
    "CAR_STOP",
    "CAR_PASS",
    "CAR_CRASH",
    "SIREN",
    "TRAIN",
    "JETPLANE",
    "STARSHIP",
    "BURST_NOISE",
    "APPLAUSE",
    "LAUGHING",
    "SCREAMING",
    "PUNCH",
    "HEART_BEAT",
    "FOOTSTEPS",
    "GUN_SHOT",
    "MACHINE_GUN",
    "LASERGUN",
    "EXPLOSION",
]


ACOUSTIC_GRAND_PIANO: int = make_instrument(1, 0)
"""
Instrument constant for Acoustic Grand Piano.

This constant corresponds to the General MIDI Level 2 patch 1, bank 0.
"""


WIDE_ACOUSTIC_GRAND: int = make_instrument(1, 1)
"""
Instrument constant for Wide Acoustic Grand.

This constant corresponds to the General MIDI Level 2 patch 1, bank 1.
"""


DARK_ACOUSTIC_GRAND: int = make_instrument(1, 2)
"""
Instrument constant for Dark Acoustic Grand.

This constant corresponds to the General MIDI Level 2 patch 1, bank 2.
"""


BRIGHT_ACOUSTIC_PIANO: int = make_instrument(2, 0)
"""
Instrument constant for Bright Acoustic Piano.

This constant corresponds to the General MIDI Level 2 patch 2, bank 0.
"""


WIDE_BRIGHT_ACOUSTIC: int = make_instrument(2, 1)
"""
Instrument constant for Wide Bright Acoustic.

This constant corresponds to the General MIDI Level 2 patch 2, bank 1.
"""


ELECTRIC_GRAND_PIANO: int = make_instrument(3, 0)
"""
Instrument constant for Electric Grand Piano.

This constant corresponds to the General MIDI Level 2 patch 3, bank 0.
"""


WIDE_ELECTRIC_GRAND: int = make_instrument(3, 1)
"""
Instrument constant for Wide Electric Grand.

This constant corresponds to the General MIDI Level 2 patch 3, bank 1.
"""


HONKY_TONK_PIANO: int = make_instrument(4, 0)
"""
Instrument constant for Honky-tonk Piano.

This constant corresponds to the General MIDI Level 2 patch 4, bank 0.
"""


WIDE_HONKY_TONK: int = make_instrument(4, 1)
"""
Instrument constant for Wide Honky-tonk.

This constant corresponds to the General MIDI Level 2 patch 4, bank 1.
"""


RHODES_PIANO: int = make_instrument(5, 0)
"""
Instrument constant for Rhodes Piano.

This constant corresponds to the General MIDI Level 2 patch 5, bank 0.
"""


DETUNED_ELECTRIC_PIANO_1: int = make_instrument(5, 1)
"""
Instrument constant for Detuned Electric Piano 1.

This constant corresponds to the General MIDI Level 2 patch 5, bank 1.
"""


ELECTRIC_PIANO_1_VARIATION: int = make_instrument(5, 2)
"""
Instrument constant for Electric Piano 1 Variation.

This constant corresponds to the General MIDI Level 2 patch 5, bank 2.
"""


ELECTRIC_PIANO_60S: int = make_instrument(5, 3)
"""
Instrument constant for Electric Piano 60's.

This constant corresponds to the General MIDI Level 2 patch 5, bank 3.
"""


CHORUSED_ELECTRIC_PIANO: int = make_instrument(6, 0)
"""
Instrument constant for Chorused Electric Piano.

This constant corresponds to the General MIDI Level 2 patch 6, bank 0.
"""


DETUNED_ELECTRIC_PIANO_2: int = make_instrument(6, 1)
"""
Instrument constant for Detuned Electric Piano 2.

This constant corresponds to the General MIDI Level 2 patch 6, bank 1.
"""


ELECTRIC_PIANO_2_VARIATION: int = make_instrument(6, 2)
"""
Instrument constant for Electric Piano 2 Variation.

This constant corresponds to the General MIDI Level 2 patch 6, bank 2.
"""


ELECTRIC_PIANO_LEGEND: int = make_instrument(6, 3)
"""
Instrument constant for Electric Piano Legend.

This constant corresponds to the General MIDI Level 2 patch 6, bank 3.
"""


ELECTRIC_PIANO_PHASE: int = make_instrument(6, 4)
"""
Instrument constant for Electric Piano Phase.

This constant corresponds to the General MIDI Level 2 patch 6, bank 4.
"""


HARPSICHORD: int = make_instrument(7, 0)
"""
Instrument constant for Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 0.
"""


COUPLED_HARPSICHORD: int = make_instrument(7, 1)
"""
Instrument constant for Coupled Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 1.
"""


WIDE_HARPSICHORD: int = make_instrument(7, 2)
"""
Instrument constant for Wide Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 2.
"""


OPEN_HARPSICHORD: int = make_instrument(7, 3)
"""
Instrument constant for Open Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 3.
"""


CLAVINET: int = make_instrument(8, 0)
"""
Instrument constant for Clavinet.

This constant corresponds to the General MIDI Level 2 patch 8, bank 0.
"""


PULSE_CLAVINET: int = make_instrument(8, 1)
"""
Instrument constant for Pulse Clavinet .

This constant corresponds to the General MIDI Level 2 patch 8, bank 1.
"""


ACOUSTIC_GRAND_PIANO: int = make_instrument(1, 0)
"""
Instrument constant for Acoustic Grand Piano.

This constant corresponds to the General MIDI Level 2 patch 1, bank 0.
"""


WIDE_ACOUSTIC_GRAND: int = make_instrument(1, 1)
"""
Instrument constant for Wide Acoustic Grand.

This constant corresponds to the General MIDI Level 2 patch 1, bank 1.
"""


DARK_ACOUSTIC_GRAND: int = make_instrument(1, 2)
"""
Instrument constant for Dark Acoustic Grand.

This constant corresponds to the General MIDI Level 2 patch 1, bank 2.
"""


BRIGHT_ACOUSTIC_PIANO: int = make_instrument(2, 0)
"""
Instrument constant for Bright Acoustic Piano.

This constant corresponds to the General MIDI Level 2 patch 2, bank 0.
"""


WIDE_BRIGHT_ACOUSTIC: int = make_instrument(2, 1)
"""
Instrument constant for Wide Bright Acoustic.

This constant corresponds to the General MIDI Level 2 patch 2, bank 1.
"""


ELECTRIC_GRAND_PIANO: int = make_instrument(3, 0)
"""
Instrument constant for Electric Grand Piano.

This constant corresponds to the General MIDI Level 2 patch 3, bank 0.
"""


WIDE_ELECTRIC_GRAND: int = make_instrument(3, 1)
"""
Instrument constant for Wide Electric Grand.

This constant corresponds to the General MIDI Level 2 patch 3, bank 1.
"""


HONKY_TONK_PIANO: int = make_instrument(4, 0)
"""
Instrument constant for Honky-tonk Piano.

This constant corresponds to the General MIDI Level 2 patch 4, bank 0.
"""


WIDE_HONKY_TONK: int = make_instrument(4, 1)
"""
Instrument constant for Wide Honky-tonk.

This constant corresponds to the General MIDI Level 2 patch 4, bank 1.
"""


RHODES_PIANO: int = make_instrument(5, 0)
"""
Instrument constant for Rhodes Piano.

This constant corresponds to the General MIDI Level 2 patch 5, bank 0.
"""


DETUNED_ELECTRIC_PIANO_1: int = make_instrument(5, 1)
"""
Instrument constant for Detuned Electric Piano 1.

This constant corresponds to the General MIDI Level 2 patch 5, bank 1.
"""


ELECTRIC_PIANO_1_VARIATION: int = make_instrument(5, 2)
"""
Instrument constant for Electric Piano 1 Variation.

This constant corresponds to the General MIDI Level 2 patch 5, bank 2.
"""


ELECTRIC_PIANO_60S: int = make_instrument(5, 3)
"""
Instrument constant for Electric Piano 60's.

This constant corresponds to the General MIDI Level 2 patch 5, bank 3.
"""


CHORUSED_ELECTRIC_PIANO: int = make_instrument(6, 0)
"""
Instrument constant for Chorused Electric Piano.

This constant corresponds to the General MIDI Level 2 patch 6, bank 0.
"""


DETUNED_ELECTRIC_PIANO_2: int = make_instrument(6, 1)
"""
Instrument constant for Detuned Electric Piano 2.

This constant corresponds to the General MIDI Level 2 patch 6, bank 1.
"""


ELECTRIC_PIANO_2_VARIATION: int = make_instrument(6, 2)
"""
Instrument constant for Electric Piano 2 Variation.

This constant corresponds to the General MIDI Level 2 patch 6, bank 2.
"""


ELECTRIC_PIANO_LEGEND: int = make_instrument(6, 3)
"""
Instrument constant for Electric Piano Legend.

This constant corresponds to the General MIDI Level 2 patch 6, bank 3.
"""


ELECTRIC_PIANO_PHASE: int = make_instrument(6, 4)
"""
Instrument constant for Electric Piano Phase.

This constant corresponds to the General MIDI Level 2 patch 6, bank 4.
"""


HARPSICHORD: int = make_instrument(7, 0)
"""
Instrument constant for Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 0.
"""


COUPLED_HARPSICHORD: int = make_instrument(7, 1)
"""
Instrument constant for Coupled Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 1.
"""


WIDE_HARPSICHORD: int = make_instrument(7, 2)
"""
Instrument constant for Wide Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 2.
"""


OPEN_HARPSICHORD: int = make_instrument(7, 3)
"""
Instrument constant for Open Harpsichord.

This constant corresponds to the General MIDI Level 2 patch 7, bank 3.
"""


CLAVINET: int = make_instrument(8, 0)
"""
Instrument constant for Clavinet.

This constant corresponds to the General MIDI Level 2 patch 8, bank 0.
"""


PULSE_CLAVINET: int = make_instrument(8, 1)
"""
Instrument constant for Pulse Clavinet .

This constant corresponds to the General MIDI Level 2 patch 8, bank 1.
"""


CELESTA: int = make_instrument(9, 0)
"""
Instrument constant for Celesta.

This constant corresponds to the General MIDI Level 2 patch 9, bank 0.
"""


GLOCKENSPIEL: int = make_instrument(10, 0)
"""
Instrument constant for Glockenspiel.

This constant corresponds to the General MIDI Level 2 patch 10, bank 0.
"""


MUSIC_BOX: int = make_instrument(11, 0)
"""
Instrument constant for Music Box.

This constant corresponds to the General MIDI Level 2 patch 11, bank 0.
"""


VIBRAPHONE: int = make_instrument(12, 0)
"""
Instrument constant for Vibraphone.

This constant corresponds to the General MIDI Level 2 patch 12, bank 0.
"""


WET_VIBRAPHONE: int = make_instrument(12, 1)
"""
Instrument constant for Wet Vibraphone.

This constant corresponds to the General MIDI Level 2 patch 12, bank 1.
"""


MARIMBA: int = make_instrument(13, 0)
"""
Instrument constant for Marimba.

This constant corresponds to the General MIDI Level 2 patch 13, bank 0.
"""


WIDE_MARIMBA: int = make_instrument(13, 1)
"""
Instrument constant for Wide Marimba.

This constant corresponds to the General MIDI Level 2 patch 13, bank 1.
"""


XYLOPHONE: int = make_instrument(14, 0)
"""
Instrument constant for Xylophone.

This constant corresponds to the General MIDI Level 2 patch 14, bank 0.
"""


TUBULAR_BELL: int = make_instrument(15, 0)
"""
Instrument constant for Tubular Bell.

This constant corresponds to the General MIDI Level 2 patch 15, bank 0.
"""


CHURCH_BELL: int = make_instrument(15, 1)
"""
Instrument constant for Church Bell.

This constant corresponds to the General MIDI Level 2 patch 15, bank 1.
"""


CARILLON: int = make_instrument(15, 2)
"""
Instrument constant for Carillon.

This constant corresponds to the General MIDI Level 2 patch 15, bank 2.
"""


DULCIMER: int = make_instrument(16, 0)
"""
Instrument constant for Dulcimer.

This constant corresponds to the General MIDI Level 2 patch 16, bank 0.
"""


DRAWBAR_ORGAN: int = make_instrument(17, 0)
"""
Instrument constant for Drawbar Organ.

This constant corresponds to the General MIDI Level 2 patch 17, bank 0.
"""


DETUNED_ORGAN_1: int = make_instrument(17, 1)
"""
Instrument constant for Detuned Organ 1.

This constant corresponds to the General MIDI Level 2 patch 17, bank 1.
"""


ORGAN_1_60S: int = make_instrument(17, 2)
"""
Instrument constant for Organ 1 60's.

This constant corresponds to the General MIDI Level 2 patch 17, bank 2.
"""


ORGAN_4: int = make_instrument(17, 3)
"""
Instrument constant for Organ 4.

This constant corresponds to the General MIDI Level 2 patch 17, bank 3.
"""


PERCUSSIVE_B3_ORGAN: int = make_instrument(18, 0)
"""
Instrument constant for Percussive B3 Organ.

This constant corresponds to the General MIDI Level 2 patch 18, bank 0.
"""


DETUNED_ORGAN_2: int = make_instrument(18, 1)
"""
Instrument constant for Detuned Organ 2.

This constant corresponds to the General MIDI Level 2 patch 18, bank 1.
"""


ORGAN_5: int = make_instrument(18, 2)
"""
Instrument constant for Organ 5.

This constant corresponds to the General MIDI Level 2 patch 18, bank 2.
"""


ROCK_ORGAN: int = make_instrument(19, 0)
"""
Instrument constant for Rock Organ.

This constant corresponds to the General MIDI Level 2 patch 19, bank 0.
"""


CHURCH_ORGAN_1: int = make_instrument(20, 0)
"""
Instrument constant for Church Organ 1.

This constant corresponds to the General MIDI Level 2 patch 20, bank 0.
"""


CHURCH_ORGAN_2: int = make_instrument(20, 1)
"""
Instrument constant for Church Organ 2.

This constant corresponds to the General MIDI Level 2 patch 20, bank 1.
"""


CHURCH_ORGAN_3: int = make_instrument(20, 2)
"""
Instrument constant for Church Organ 3.

This constant corresponds to the General MIDI Level 2 patch 20, bank 2.
"""


REED_ORGAN: int = make_instrument(21, 0)
"""
Instrument constant for Reed Organ.

This constant corresponds to the General MIDI Level 2 patch 21, bank 0.
"""


PUFF_ORGAN: int = make_instrument(21, 1)
"""
Instrument constant for Puff Organ.

This constant corresponds to the General MIDI Level 2 patch 21, bank 1.
"""


FRENCH_ACCORDION: int = make_instrument(22, 0)
"""
Instrument constant for French Accordion.

This constant corresponds to the General MIDI Level 2 patch 22, bank 0.
"""


ITALIAN_ACCORDION: int = make_instrument(22, 1)
"""
Instrument constant for Italian Accordion.

This constant corresponds to the General MIDI Level 2 patch 22, bank 1.
"""


HARMONICA: int = make_instrument(23, 0)
"""
Instrument constant for Harmonica.

This constant corresponds to the General MIDI Level 2 patch 23, bank 0.
"""


BANDONEON: int = make_instrument(24, 0)
"""
Instrument constant for Bandoneon.

This constant corresponds to the General MIDI Level 2 patch 24, bank 0.
"""


NYLON_STRING_GUITAR: int = make_instrument(25, 0)
"""
Instrument constant for Nylon-String Guitar.

This constant corresponds to the General MIDI Level 2 patch 25, bank 0.
"""


UKULELE: int = make_instrument(25, 1)
"""
Instrument constant for Ukulele.

This constant corresponds to the General MIDI Level 2 patch 25, bank 1.
"""


OPEN_NYLON_GUITAR: int = make_instrument(25, 2)
"""
Instrument constant for Open Nylon Guitar.

This constant corresponds to the General MIDI Level 2 patch 25, bank 2.
"""


NYLON_GUITAR_2: int = make_instrument(25, 3)
"""
Instrument constant for Nylon Guitar 2.

This constant corresponds to the General MIDI Level 2 patch 25, bank 3.
"""


STEEL_STRING_GUITAR: int = make_instrument(26, 0)
"""
Instrument constant for Steel-String Guitar.

This constant corresponds to the General MIDI Level 2 patch 26, bank 0.
"""


GUITAR_12_STRING: int = make_instrument(26, 1)
"""
Instrument constant for Guitar 12-String.

This constant corresponds to the General MIDI Level 2 patch 26, bank 1.
"""


MANDOLIN: int = make_instrument(26, 2)
"""
Instrument constant for Mandolin.

This constant corresponds to the General MIDI Level 2 patch 26, bank 2.
"""


STEEL__BODY: int = make_instrument(26, 3)
"""
Instrument constant for Steel + Body.

This constant corresponds to the General MIDI Level 2 patch 26, bank 3.
"""


JAZZ_GUITAR: int = make_instrument(27, 0)
"""
Instrument constant for Jazz Guitar.

This constant corresponds to the General MIDI Level 2 patch 27, bank 0.
"""


HAWAIIAN_GUITAR: int = make_instrument(27, 1)
"""
Instrument constant for Hawaiian Guitar.

This constant corresponds to the General MIDI Level 2 patch 27, bank 1.
"""


CLEAN_ELECTRIC_GUITAR: int = make_instrument(28, 0)
"""
Instrument constant for Clean Electric Guitar.

This constant corresponds to the General MIDI Level 2 patch 28, bank 0.
"""


CHORUS_GUITAR: int = make_instrument(28, 1)
"""
Instrument constant for Chorus Guitar.

This constant corresponds to the General MIDI Level 2 patch 28, bank 1.
"""


MID_TONE_GUITAR: int = make_instrument(28, 2)
"""
Instrument constant for Mid Tone Guitar.

This constant corresponds to the General MIDI Level 2 patch 28, bank 2.
"""


MUTED_ELECTRIC_GUITAR: int = make_instrument(29, 0)
"""
Instrument constant for Muted Electric Guitar.

This constant corresponds to the General MIDI Level 2 patch 29, bank 0.
"""


FUNK_GUITAR: int = make_instrument(29, 1)
"""
Instrument constant for Funk Guitar.

This constant corresponds to the General MIDI Level 2 patch 29, bank 1.
"""


FUNK_GUITAR_2: int = make_instrument(29, 2)
"""
Instrument constant for Funk Guitar 2.

This constant corresponds to the General MIDI Level 2 patch 29, bank 2.
"""


JAZZ_MAN: int = make_instrument(29, 3)
"""
Instrument constant for Jazz Man.

This constant corresponds to the General MIDI Level 2 patch 29, bank 3.
"""


OVERDRIVEN_GUITAR: int = make_instrument(30, 0)
"""
Instrument constant for Overdriven Guitar.

This constant corresponds to the General MIDI Level 2 patch 30, bank 0.
"""


GUITAR_PINCH: int = make_instrument(30, 1)
"""
Instrument constant for Guitar Pinch.

This constant corresponds to the General MIDI Level 2 patch 30, bank 1.
"""


DISTORTION_GUITAR: int = make_instrument(31, 0)
"""
Instrument constant for Distortion Guitar.

This constant corresponds to the General MIDI Level 2 patch 31, bank 0.
"""


FEEDBACK_GUITAR: int = make_instrument(31, 1)
"""
Instrument constant for Feedback Guitar.

This constant corresponds to the General MIDI Level 2 patch 31, bank 1.
"""


DISTORTION_RTM_GUITAR: int = make_instrument(31, 2)
"""
Instrument constant for Distortion Rtm Guitar.

This constant corresponds to the General MIDI Level 2 patch 31, bank 2.
"""


GUITAR_HARMONICS: int = make_instrument(32, 0)
"""
Instrument constant for Guitar Harmonics.

This constant corresponds to the General MIDI Level 2 patch 32, bank 0.
"""


GUITAR_FEEDBACK: int = make_instrument(32, 1)
"""
Instrument constant for Guitar Feedback.

This constant corresponds to the General MIDI Level 2 patch 32, bank 1.
"""


ACOUSTIC_BASS: int = make_instrument(33, 0)
"""
Instrument constant for Acoustic Bass.

This constant corresponds to the General MIDI Level 2 patch 33, bank 0.
"""


FINGERED_BASS: int = make_instrument(34, 0)
"""
Instrument constant for Fingered Bass.

This constant corresponds to the General MIDI Level 2 patch 34, bank 0.
"""


FINGER_SLAP: int = make_instrument(34, 1)
"""
Instrument constant for Finger Slap.

This constant corresponds to the General MIDI Level 2 patch 34, bank 1.
"""


PICKED_BASS: int = make_instrument(35, 0)
"""
Instrument constant for Picked Bass.

This constant corresponds to the General MIDI Level 2 patch 35, bank 0.
"""


FRETLESS_BASS: int = make_instrument(36, 0)
"""
Instrument constant for Fretless Bass.

This constant corresponds to the General MIDI Level 2 patch 36, bank 0.
"""


SLAP_BASS_1: int = make_instrument(37, 0)
"""
Instrument constant for Slap Bass 1.

This constant corresponds to the General MIDI Level 2 patch 37, bank 0.
"""


SLAP_BASS_2: int = make_instrument(38, 0)
"""
Instrument constant for Slap Bass 2.

This constant corresponds to the General MIDI Level 2 patch 38, bank 0.
"""


SYNTH_BASS_1: int = make_instrument(39, 0)
"""
Instrument constant for Synth Bass 1.

This constant corresponds to the General MIDI Level 2 patch 39, bank 0.
"""


SYNTH_BASS_101: int = make_instrument(39, 1)
"""
Instrument constant for Synth Bass 101.

This constant corresponds to the General MIDI Level 2 patch 39, bank 1.
"""


SYNTH_BASS_3: int = make_instrument(39, 2)
"""
Instrument constant for Synth Bass 3.

This constant corresponds to the General MIDI Level 2 patch 39, bank 2.
"""


CLAVI_BASS: int = make_instrument(39, 3)
"""
Instrument constant for Clavi Bass.

This constant corresponds to the General MIDI Level 2 patch 39, bank 3.
"""


HAMMER: int = make_instrument(39, 4)
"""
Instrument constant for Hammer.

This constant corresponds to the General MIDI Level 2 patch 39, bank 4.
"""


SYNTH_BASS_2: int = make_instrument(40, 0)
"""
Instrument constant for Synth Bass 2.

This constant corresponds to the General MIDI Level 2 patch 40, bank 0.
"""


SYNTH_BASS_4: int = make_instrument(40, 1)
"""
Instrument constant for Synth Bass 4.

This constant corresponds to the General MIDI Level 2 patch 40, bank 1.
"""


RUBBER_BASS: int = make_instrument(40, 2)
"""
Instrument constant for Rubber Bass.

This constant corresponds to the General MIDI Level 2 patch 40, bank 2.
"""


ATTACK_PULSE: int = make_instrument(40, 3)
"""
Instrument constant for Attack Pulse.

This constant corresponds to the General MIDI Level 2 patch 40, bank 3.
"""


VIOLIN: int = make_instrument(41, 0)
"""
Instrument constant for Violin.

This constant corresponds to the General MIDI Level 2 patch 41, bank 0.
"""


SLOW_VIOLIN: int = make_instrument(41, 1)
"""
Instrument constant for Slow Violin.

This constant corresponds to the General MIDI Level 2 patch 41, bank 1.
"""


VIOLA: int = make_instrument(42, 0)
"""
Instrument constant for Viola.

This constant corresponds to the General MIDI Level 2 patch 42, bank 0.
"""


CELLO: int = make_instrument(43, 0)
"""
Instrument constant for Cello.

This constant corresponds to the General MIDI Level 2 patch 43, bank 0.
"""


CONTRABASS: int = make_instrument(44, 0)
"""
Instrument constant for Contrabass.

This constant corresponds to the General MIDI Level 2 patch 44, bank 0.
"""


TREMOLO_STRINGS: int = make_instrument(45, 0)
"""
Instrument constant for Tremolo Strings.

This constant corresponds to the General MIDI Level 2 patch 45, bank 0.
"""


PIZZICATO_STRINGS: int = make_instrument(46, 0)
"""
Instrument constant for Pizzicato Strings.

This constant corresponds to the General MIDI Level 2 patch 46, bank 0.
"""


HARP: int = make_instrument(47, 0)
"""
Instrument constant for Harp.

This constant corresponds to the General MIDI Level 2 patch 47, bank 0.
"""


YANG_QIN: int = make_instrument(47, 1)
"""
Instrument constant for Yang Qin.

This constant corresponds to the General MIDI Level 2 patch 47, bank 1.
"""


TIMPANI: int = make_instrument(48, 0)
"""
Instrument constant for Timpani.

This constant corresponds to the General MIDI Level 2 patch 48, bank 0.
"""


STRING_ENSEMBLE: int = make_instrument(49, 0)
"""
Instrument constant for String Ensemble.

This constant corresponds to the General MIDI Level 2 patch 49, bank 0.
"""


ORCHESTRA_STRINGS: int = make_instrument(49, 1)
"""
Instrument constant for Orchestra Strings.

This constant corresponds to the General MIDI Level 2 patch 49, bank 1.
"""


STRINGS_60S: int = make_instrument(49, 2)
"""
Instrument constant for Strings 60's.

This constant corresponds to the General MIDI Level 2 patch 49, bank 2.
"""


SLOW_STRING_ENSEMBLE: int = make_instrument(50, 0)
"""
Instrument constant for Slow String Ensemble.

This constant corresponds to the General MIDI Level 2 patch 50, bank 0.
"""


SYNTH_STRINGS_1: int = make_instrument(51, 0)
"""
Instrument constant for Synth Strings 1.

This constant corresponds to the General MIDI Level 2 patch 51, bank 0.
"""


SYNTH_STRINGS_3: int = make_instrument(51, 1)
"""
Instrument constant for Synth Strings 3.

This constant corresponds to the General MIDI Level 2 patch 51, bank 1.
"""


SYNTH_STRINGS_2: int = make_instrument(52, 0)
"""
Instrument constant for Synth Strings 2.

This constant corresponds to the General MIDI Level 2 patch 52, bank 0.
"""


CHOIR_AAHS: int = make_instrument(53, 0)
"""
Instrument constant for Choir Aahs.

This constant corresponds to the General MIDI Level 2 patch 53, bank 0.
"""


CHOIR_AAHS_2: int = make_instrument(53, 1)
"""
Instrument constant for Choir Aahs 2.

This constant corresponds to the General MIDI Level 2 patch 53, bank 1.
"""


VOICE_OOHS: int = make_instrument(54, 0)
"""
Instrument constant for Voice Oohs.

This constant corresponds to the General MIDI Level 2 patch 54, bank 0.
"""


HUMMING: int = make_instrument(54, 1)
"""
Instrument constant for Humming.

This constant corresponds to the General MIDI Level 2 patch 54, bank 1.
"""


SYNTH_VOICE: int = make_instrument(55, 0)
"""
Instrument constant for Synth Voice.

This constant corresponds to the General MIDI Level 2 patch 55, bank 0.
"""


ANALOG_VOICE: int = make_instrument(55, 1)
"""
Instrument constant for Analog Voice.

This constant corresponds to the General MIDI Level 2 patch 55, bank 1.
"""


ORCHESTRA_HIT: int = make_instrument(56, 0)
"""
Instrument constant for Orchestra Hit.

This constant corresponds to the General MIDI Level 2 patch 56, bank 0.
"""


BASS_HIT: int = make_instrument(56, 1)
"""
Instrument constant for Bass Hit.

This constant corresponds to the General MIDI Level 2 patch 56, bank 1.
"""


HIT_6TH: int = make_instrument(56, 2)
"""
Instrument constant for Hit 6th.

This constant corresponds to the General MIDI Level 2 patch 56, bank 2.
"""


EURO_HIT: int = make_instrument(56, 3)
"""
Instrument constant for Euro Hit.

This constant corresponds to the General MIDI Level 2 patch 56, bank 3.
"""


TRUMPET: int = make_instrument(57, 0)
"""
Instrument constant for Trumpet.

This constant corresponds to the General MIDI Level 2 patch 57, bank 0.
"""


DARK_TRUMPET: int = make_instrument(57, 1)
"""
Instrument constant for Dark Trumpet.

This constant corresponds to the General MIDI Level 2 patch 57, bank 1.
"""


TROMBONE: int = make_instrument(58, 0)
"""
Instrument constant for Trombone.

This constant corresponds to the General MIDI Level 2 patch 58, bank 0.
"""


TROMBONE_2: int = make_instrument(58, 1)
"""
Instrument constant for Trombone 2.

This constant corresponds to the General MIDI Level 2 patch 58, bank 1.
"""


BRIGHT_TROMBONE: int = make_instrument(58, 2)
"""
Instrument constant for Bright Trombone.

This constant corresponds to the General MIDI Level 2 patch 58, bank 2.
"""


TUBA: int = make_instrument(59, 0)
"""
Instrument constant for Tuba.

This constant corresponds to the General MIDI Level 2 patch 59, bank 0.
"""


MUTED_TRUMPET: int = make_instrument(60, 0)
"""
Instrument constant for Muted Trumpet.

This constant corresponds to the General MIDI Level 2 patch 60, bank 0.
"""


MUTED_TRUMPET_2: int = make_instrument(60, 1)
"""
Instrument constant for Muted Trumpet 2.

This constant corresponds to the General MIDI Level 2 patch 60, bank 1.
"""


FRENCH_HORNS: int = make_instrument(61, 0)
"""
Instrument constant for French Horns.

This constant corresponds to the General MIDI Level 2 patch 61, bank 0.
"""


FRENCH_HORN_2: int = make_instrument(61, 1)
"""
Instrument constant for French Horn 2.

This constant corresponds to the General MIDI Level 2 patch 61, bank 1.
"""


BRASS_SECTION_1: int = make_instrument(62, 0)
"""
Instrument constant for Brass Section 1.

This constant corresponds to the General MIDI Level 2 patch 62, bank 0.
"""


BRASS_SECTION_2: int = make_instrument(62, 1)
"""
Instrument constant for Brass Section 2.

This constant corresponds to the General MIDI Level 2 patch 62, bank 1.
"""


SYNTH_BRASS_1: int = make_instrument(63, 0)
"""
Instrument constant for Synth Brass 1.

This constant corresponds to the General MIDI Level 2 patch 63, bank 0.
"""


SYNTH_BRASS_3: int = make_instrument(63, 1)
"""
Instrument constant for Synth Brass 3.

This constant corresponds to the General MIDI Level 2 patch 63, bank 1.
"""


ANALOG_BRASS_1: int = make_instrument(63, 2)
"""
Instrument constant for Analog Brass 1.

This constant corresponds to the General MIDI Level 2 patch 63, bank 2.
"""


JUMP_BRASS: int = make_instrument(63, 3)
"""
Instrument constant for Jump Brass.

This constant corresponds to the General MIDI Level 2 patch 63, bank 3.
"""


SYNTH_BRASS_2: int = make_instrument(64, 0)
"""
Instrument constant for Synth Brass 2.

This constant corresponds to the General MIDI Level 2 patch 64, bank 0.
"""


SYNTH_BRASS_4: int = make_instrument(64, 1)
"""
Instrument constant for Synth Brass 4.

This constant corresponds to the General MIDI Level 2 patch 64, bank 1.
"""


ANALOG_BRASS_2: int = make_instrument(64, 2)
"""
Instrument constant for Analog Brass 2.

This constant corresponds to the General MIDI Level 2 patch 64, bank 2.
"""


SOPRANO_SAX: int = make_instrument(65, 0)
"""
Instrument constant for Soprano Sax.

This constant corresponds to the General MIDI Level 2 patch 65, bank 0.
"""


ALTO_SAX: int = make_instrument(66, 0)
"""
Instrument constant for Alto Sax.

This constant corresponds to the General MIDI Level 2 patch 66, bank 0.
"""


TENOR_SAX: int = make_instrument(67, 0)
"""
Instrument constant for Tenor Sax.

This constant corresponds to the General MIDI Level 2 patch 67, bank 0.
"""


BARITONE_SAX: int = make_instrument(68, 0)
"""
Instrument constant for Baritone Sax.

This constant corresponds to the General MIDI Level 2 patch 68, bank 0.
"""


OBOE: int = make_instrument(69, 0)
"""
Instrument constant for Oboe.

This constant corresponds to the General MIDI Level 2 patch 69, bank 0.
"""


ENGLISH_HORN: int = make_instrument(70, 0)
"""
Instrument constant for English Horn.

This constant corresponds to the General MIDI Level 2 patch 70, bank 0.
"""


BASSOON: int = make_instrument(71, 0)
"""
Instrument constant for Bassoon.

This constant corresponds to the General MIDI Level 2 patch 71, bank 0.
"""


CLARINET: int = make_instrument(72, 0)
"""
Instrument constant for Clarinet.

This constant corresponds to the General MIDI Level 2 patch 72, bank 0.
"""


PICCOLO: int = make_instrument(73, 0)
"""
Instrument constant for Piccolo.

This constant corresponds to the General MIDI Level 2 patch 73, bank 0.
"""


FLUTE: int = make_instrument(74, 0)
"""
Instrument constant for Flute.

This constant corresponds to the General MIDI Level 2 patch 74, bank 0.
"""


RECORDER: int = make_instrument(75, 0)
"""
Instrument constant for Recorder.

This constant corresponds to the General MIDI Level 2 patch 75, bank 0.
"""


PAN_FLUTE: int = make_instrument(76, 0)
"""
Instrument constant for Pan Flute.

This constant corresponds to the General MIDI Level 2 patch 76, bank 0.
"""


BOTTLE_BLOW: int = make_instrument(77, 0)
"""
Instrument constant for Bottle Blow.

This constant corresponds to the General MIDI Level 2 patch 77, bank 0.
"""


SHAKUHACHI: int = make_instrument(78, 0)
"""
Instrument constant for Shakuhachi.

This constant corresponds to the General MIDI Level 2 patch 78, bank 0.
"""


WHISTLE: int = make_instrument(79, 0)
"""
Instrument constant for Whistle.

This constant corresponds to the General MIDI Level 2 patch 79, bank 0.
"""


OCARINA: int = make_instrument(80, 0)
"""
Instrument constant for Ocarina.

This constant corresponds to the General MIDI Level 2 patch 80, bank 0.
"""


SQUARE_LEAD: int = make_instrument(81, 0)
"""
Instrument constant for Square Lead.

This constant corresponds to the General MIDI Level 2 patch 81, bank 0.
"""


SQUARE_WAVE: int = make_instrument(81, 1)
"""
Instrument constant for Square Wave.

This constant corresponds to the General MIDI Level 2 patch 81, bank 1.
"""


SINE_WAVE: int = make_instrument(81, 2)
"""
Instrument constant for Sine Wave.

This constant corresponds to the General MIDI Level 2 patch 81, bank 2.
"""


SAW_LEAD: int = make_instrument(82, 0)
"""
Instrument constant for Saw Lead.

This constant corresponds to the General MIDI Level 2 patch 82, bank 0.
"""


SAW_WAVE: int = make_instrument(82, 1)
"""
Instrument constant for Saw Wave.

This constant corresponds to the General MIDI Level 2 patch 82, bank 1.
"""


DOCTOR_SOLO: int = make_instrument(82, 2)
"""
Instrument constant for Doctor Solo.

This constant corresponds to the General MIDI Level 2 patch 82, bank 2.
"""


NATURAL_LEAD: int = make_instrument(82, 3)
"""
Instrument constant for Natural Lead.

This constant corresponds to the General MIDI Level 2 patch 82, bank 3.
"""


SEQUENCED_SAW: int = make_instrument(82, 4)
"""
Instrument constant for Sequenced Saw.

This constant corresponds to the General MIDI Level 2 patch 82, bank 4.
"""


SYNTH_CALLIOPE: int = make_instrument(83, 0)
"""
Instrument constant for Synth Calliope.

This constant corresponds to the General MIDI Level 2 patch 83, bank 0.
"""


CHIFFER_LEAD: int = make_instrument(84, 0)
"""
Instrument constant for Chiffer Lead.

This constant corresponds to the General MIDI Level 2 patch 84, bank 0.
"""


CHARANG: int = make_instrument(85, 0)
"""
Instrument constant for Charang.

This constant corresponds to the General MIDI Level 2 patch 85, bank 0.
"""


WIRE_LEAD: int = make_instrument(85, 1)
"""
Instrument constant for Wire Lead.

This constant corresponds to the General MIDI Level 2 patch 85, bank 1.
"""


SOLO_SYNTH_VOX: int = make_instrument(86, 0)
"""
Instrument constant for Solo Synth Vox.

This constant corresponds to the General MIDI Level 2 patch 86, bank 0.
"""


SAW_WAVE_5TH: int = make_instrument(87, 0)
"""
Instrument constant for Saw Wave 5th.

This constant corresponds to the General MIDI Level 2 patch 87, bank 0.
"""


BASS__LEAD: int = make_instrument(88, 0)
"""
Instrument constant for Bass & Lead.

This constant corresponds to the General MIDI Level 2 patch 88, bank 0.
"""


DELAYED_LEAD: int = make_instrument(88, 1)
"""
Instrument constant for Delayed Lead .

This constant corresponds to the General MIDI Level 2 patch 88, bank 1.
"""


ICE_RAIN: int = make_instrument(97, 0)
"""
Instrument constant for Ice Rain.

This constant corresponds to the General MIDI Level 2 patch 97, bank 0.
"""


SOUNDTRACK: int = make_instrument(98, 0)
"""
Instrument constant for Soundtrack.

This constant corresponds to the General MIDI Level 2 patch 98, bank 0.
"""


CRYSTAL: int = make_instrument(99, 0)
"""
Instrument constant for Crystal.

This constant corresponds to the General MIDI Level 2 patch 99, bank 0.
"""


SYNTH_MALLET: int = make_instrument(99, 1)
"""
Instrument constant for Synth Mallet.

This constant corresponds to the General MIDI Level 2 patch 99, bank 1.
"""


ATMOSPHERE: int = make_instrument(100, 0)
"""
Instrument constant for Atmosphere.

This constant corresponds to the General MIDI Level 2 patch 100, bank 0.
"""


BRIGHTNESS: int = make_instrument(101, 0)
"""
Instrument constant for Brightness.

This constant corresponds to the General MIDI Level 2 patch 101, bank 0.
"""


GOBLIN: int = make_instrument(102, 0)
"""
Instrument constant for Goblin.

This constant corresponds to the General MIDI Level 2 patch 102, bank 0.
"""


ECHO_DROPS: int = make_instrument(103, 0)
"""
Instrument constant for Echo Drops.

This constant corresponds to the General MIDI Level 2 patch 103, bank 0.
"""


ECHO_BELL: int = make_instrument(103, 1)
"""
Instrument constant for Echo Bell.

This constant corresponds to the General MIDI Level 2 patch 103, bank 1.
"""


ECHO_PAN: int = make_instrument(103, 2)
"""
Instrument constant for Echo Pan.

This constant corresponds to the General MIDI Level 2 patch 103, bank 2.
"""


STAR_THEME: int = make_instrument(104, 0)
"""
Instrument constant for Star Theme.

This constant corresponds to the General MIDI Level 2 patch 104, bank 0.
"""


SITAR: int = make_instrument(105, 0)
"""
Instrument constant for Sitar.

This constant corresponds to the General MIDI Level 2 patch 105, bank 0.
"""


SITAR_2: int = make_instrument(105, 1)
"""
Instrument constant for Sitar 2.

This constant corresponds to the General MIDI Level 2 patch 105, bank 1.
"""


BANJO: int = make_instrument(106, 0)
"""
Instrument constant for Banjo.

This constant corresponds to the General MIDI Level 2 patch 106, bank 0.
"""


SHAMISEN: int = make_instrument(107, 0)
"""
Instrument constant for Shamisen.

This constant corresponds to the General MIDI Level 2 patch 107, bank 0.
"""


KOTO: int = make_instrument(108, 0)
"""
Instrument constant for Koto.

This constant corresponds to the General MIDI Level 2 patch 108, bank 0.
"""


TAISHO_KOTO: int = make_instrument(108, 1)
"""
Instrument constant for Taisho Koto.

This constant corresponds to the General MIDI Level 2 patch 108, bank 1.
"""


KALIMBA: int = make_instrument(109, 0)
"""
Instrument constant for Kalimba.

This constant corresponds to the General MIDI Level 2 patch 109, bank 0.
"""


BAGPIPE: int = make_instrument(110, 0)
"""
Instrument constant for Bagpipe.

This constant corresponds to the General MIDI Level 2 patch 110, bank 0.
"""


FIDDLE: int = make_instrument(111, 0)
"""
Instrument constant for Fiddle.

This constant corresponds to the General MIDI Level 2 patch 111, bank 0.
"""


SHANAI: int = make_instrument(112, 0)
"""
Instrument constant for Shanai.

This constant corresponds to the General MIDI Level 2 patch 112, bank 0.
"""


TINKLE_BELL: int = make_instrument(113, 0)
"""
Instrument constant for Tinkle Bell.

This constant corresponds to the General MIDI Level 2 patch 113, bank 0.
"""


AGOGO: int = make_instrument(114, 0)
"""
Instrument constant for Agogo.

This constant corresponds to the General MIDI Level 2 patch 114, bank 0.
"""


STEEL_DRUMS: int = make_instrument(115, 0)
"""
Instrument constant for Steel Drums.

This constant corresponds to the General MIDI Level 2 patch 115, bank 0.
"""


WOODBLOCK: int = make_instrument(116, 0)
"""
Instrument constant for Woodblock.

This constant corresponds to the General MIDI Level 2 patch 116, bank 0.
"""


CASTANETS: int = make_instrument(116, 1)
"""
Instrument constant for Castanets.

This constant corresponds to the General MIDI Level 2 patch 116, bank 1.
"""


TAIKO: int = make_instrument(117, 0)
"""
Instrument constant for Taiko.

This constant corresponds to the General MIDI Level 2 patch 117, bank 0.
"""


CONCERT_BASS_DRUM: int = make_instrument(117, 1)
"""
Instrument constant for Concert Bass Drum.

This constant corresponds to the General MIDI Level 2 patch 117, bank 1.
"""


MELODIC_TOM_1: int = make_instrument(118, 0)
"""
Instrument constant for Melodic Tom 1.

This constant corresponds to the General MIDI Level 2 patch 118, bank 0.
"""


MELODIC_TOM_2: int = make_instrument(118, 1)
"""
Instrument constant for Melodic Tom 2.

This constant corresponds to the General MIDI Level 2 patch 118, bank 1.
"""


SYNTH_DRUM: int = make_instrument(119, 0)
"""
Instrument constant for Synth Drum.

This constant corresponds to the General MIDI Level 2 patch 119, bank 0.
"""


TOM_808: int = make_instrument(119, 1)
"""
Instrument constant for Tom 808.

This constant corresponds to the General MIDI Level 2 patch 119, bank 1.
"""


ELECTRIC_PERCUSSION: int = make_instrument(119, 2)
"""
Instrument constant for Electric Percussion.

This constant corresponds to the General MIDI Level 2 patch 119, bank 2.
"""


REVERSE_CYMBAL: int = make_instrument(120, 0)
"""
Instrument constant for Reverse Cymbal.

This constant corresponds to the General MIDI Level 2 patch 120, bank 0.
"""


GUITAR_FRET_NOISE: int = make_instrument(121, 0)
"""
Instrument constant for Guitar Fret Noise.

This constant corresponds to the General MIDI Level 2 patch 121, bank 0.
"""


GUITAR_CUT_NOISE: int = make_instrument(121, 1)
"""
Instrument constant for Guitar Cut Noise.

This constant corresponds to the General MIDI Level 2 patch 121, bank 1.
"""


STRING_SLAP: int = make_instrument(121, 2)
"""
Instrument constant for String Slap.

This constant corresponds to the General MIDI Level 2 patch 121, bank 2.
"""


BREATH_NOISE: int = make_instrument(122, 0)
"""
Instrument constant for Breath Noise.

This constant corresponds to the General MIDI Level 2 patch 122, bank 0.
"""


FLUTE_KEY_CLICK: int = make_instrument(122, 1)
"""
Instrument constant for Flute Key Click.

This constant corresponds to the General MIDI Level 2 patch 122, bank 1.
"""


SEASHORE: int = make_instrument(123, 0)
"""
Instrument constant for Seashore.

This constant corresponds to the General MIDI Level 2 patch 123, bank 0.
"""


RAIN: int = make_instrument(123, 1)
"""
Instrument constant for Rain.

This constant corresponds to the General MIDI Level 2 patch 123, bank 1.
"""


THUNDER: int = make_instrument(123, 2)
"""
Instrument constant for Thunder.

This constant corresponds to the General MIDI Level 2 patch 123, bank 2.
"""


WIND: int = make_instrument(123, 3)
"""
Instrument constant for Wind.

This constant corresponds to the General MIDI Level 2 patch 123, bank 3.
"""


STREAM: int = make_instrument(123, 4)
"""
Instrument constant for Stream.

This constant corresponds to the General MIDI Level 2 patch 123, bank 4.
"""


BUBBLE: int = make_instrument(123, 5)
"""
Instrument constant for Bubble.

This constant corresponds to the General MIDI Level 2 patch 123, bank 5.
"""


BIRD: int = make_instrument(124, 0)
"""
Instrument constant for Bird.

This constant corresponds to the General MIDI Level 2 patch 124, bank 0.
"""


DOG: int = make_instrument(124, 1)
"""
Instrument constant for Dog.

This constant corresponds to the General MIDI Level 2 patch 124, bank 1.
"""


HORSE_GALLOP: int = make_instrument(124, 2)
"""
Instrument constant for Horse-Gallop.

This constant corresponds to the General MIDI Level 2 patch 124, bank 2.
"""


BIRD_2: int = make_instrument(124, 3)
"""
Instrument constant for Bird 2.

This constant corresponds to the General MIDI Level 2 patch 124, bank 3.
"""


TELEPHONE_1: int = make_instrument(125, 0)
"""
Instrument constant for Telephone 1.

This constant corresponds to the General MIDI Level 2 patch 125, bank 0.
"""


TELEPHONE_2: int = make_instrument(125, 1)
"""
Instrument constant for Telephone 2.

This constant corresponds to the General MIDI Level 2 patch 125, bank 1.
"""


DOOR_CREAKING: int = make_instrument(125, 2)
"""
Instrument constant for Door Creaking.

This constant corresponds to the General MIDI Level 2 patch 125, bank 2.
"""


DOOR_CLOSING: int = make_instrument(125, 3)
"""
Instrument constant for Door Closing.

This constant corresponds to the General MIDI Level 2 patch 125, bank 3.
"""


SCRATCH: int = make_instrument(125, 4)
"""
Instrument constant for Scratch.

This constant corresponds to the General MIDI Level 2 patch 125, bank 4.
"""


WIND_CHIMES: int = make_instrument(125, 5)
"""
Instrument constant for Wind Chimes.

This constant corresponds to the General MIDI Level 2 patch 125, bank 5.
"""


HELICOPTER: int = make_instrument(126, 0)
"""
Instrument constant for Helicopter.

This constant corresponds to the General MIDI Level 2 patch 126, bank 0.
"""


CAR_ENGINE: int = make_instrument(126, 1)
"""
Instrument constant for Car-Engine.

This constant corresponds to the General MIDI Level 2 patch 126, bank 1.
"""


CAR_STOP: int = make_instrument(126, 2)
"""
Instrument constant for Car-Stop.

This constant corresponds to the General MIDI Level 2 patch 126, bank 2.
"""


CAR_PASS: int = make_instrument(126, 3)
"""
Instrument constant for Car-Pass.

This constant corresponds to the General MIDI Level 2 patch 126, bank 3.
"""


CAR_CRASH: int = make_instrument(126, 4)
"""
Instrument constant for Car-Crash.

This constant corresponds to the General MIDI Level 2 patch 126, bank 4.
"""


SIREN: int = make_instrument(126, 5)
"""
Instrument constant for Siren.

This constant corresponds to the General MIDI Level 2 patch 126, bank 5.
"""


TRAIN: int = make_instrument(126, 6)
"""
Instrument constant for Train.

This constant corresponds to the General MIDI Level 2 patch 126, bank 6.
"""


JETPLANE: int = make_instrument(126, 7)
"""
Instrument constant for Jetplane.

This constant corresponds to the General MIDI Level 2 patch 126, bank 7.
"""


STARSHIP: int = make_instrument(126, 8)
"""
Instrument constant for Starship.

This constant corresponds to the General MIDI Level 2 patch 126, bank 8.
"""


BURST_NOISE: int = make_instrument(126, 9)
"""
Instrument constant for Burst Noise.

This constant corresponds to the General MIDI Level 2 patch 126, bank 9.
"""


APPLAUSE: int = make_instrument(127, 0)
"""
Instrument constant for Applause.

This constant corresponds to the General MIDI Level 2 patch 127, bank 0.
"""


LAUGHING: int = make_instrument(127, 1)
"""
Instrument constant for Laughing.

This constant corresponds to the General MIDI Level 2 patch 127, bank 1.
"""


SCREAMING: int = make_instrument(127, 2)
"""
Instrument constant for Screaming.

This constant corresponds to the General MIDI Level 2 patch 127, bank 2.
"""


PUNCH: int = make_instrument(127, 3)
"""
Instrument constant for Punch.

This constant corresponds to the General MIDI Level 2 patch 127, bank 3.
"""


HEART_BEAT: int = make_instrument(127, 4)
"""
Instrument constant for Heart Beat.

This constant corresponds to the General MIDI Level 2 patch 127, bank 4.
"""


FOOTSTEPS: int = make_instrument(127, 5)
"""
Instrument constant for Footsteps.

This constant corresponds to the General MIDI Level 2 patch 127, bank 5.
"""


GUN_SHOT: int = make_instrument(128, 0)
"""
Instrument constant for Gun Shot.

This constant corresponds to the General MIDI Level 2 patch 128, bank 0.
"""


MACHINE_GUN: int = make_instrument(128, 1)
"""
Instrument constant for Machine Gun.

This constant corresponds to the General MIDI Level 2 patch 128, bank 1.
"""


LASERGUN: int = make_instrument(128, 2)
"""
Instrument constant for Lasergun.

This constant corresponds to the General MIDI Level 2 patch 128, bank 2.
"""


EXPLOSION: int = make_instrument(128, 3)
"""
Instrument constant for Explosion.

This constant corresponds to the General MIDI Level 2 patch 128, bank 3.
"""
