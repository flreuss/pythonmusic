# Funktionale Anforderungen

## Hohe Priorität

Der Nutzende kann unter Nutzung der Bibliothek...

- [x] Musikdaten (Noten, Phrasen, Part, Scores) über eine DAW ohne größere Latenz wiedergeben. {5}
- [x] Musikdaten (Noten, Phrasen, Part, Scores) über einen integrierten MIDI-Synthesizer ohne größere Latenz wiedergeben. {5}
- [x] Werte von einem Bereich auf einen anderen Bereich mappen _(s. mapValue). {5}_
- [x] Tonhöhenwerte von einer Skala auf eine andere übertragen (s. mapScale) und dabei übliche Skalen als Konstanten angeben. {5}
- [x] Tonhöhe (nur wohltemperiert, s. MIDI), Tondauer (min. bis 64tel genau) und Lautstärke (als Zahl oder Konstanten à la ff, pp) auf Ebene jeder einzelnen Note festlegen, verändern und abfragen. {5}
- [x] Noten oder Akkorde zu Tonfolgen (Phrasen) gruppieren. {5}
- [x] Phrasen zu Stimmen gruppieren. {5}
- [x] Panning sowie Instrument (MIDI Instrument List Level 1+2) auf Stimmen-Ebene bei Erstellung festlegen, verändern und abfragen. {5}
- [x] Stimmen zu Partituren gruppieren. {5}
- [x] Tempo auf Partitur-Ebene als Zahl in BPM oder Konstante (adagio, andante, usw.) bei Erstellung festlegen, verändern und abfragen. {5}
- [x] höhere Musikdatenstrukturen (Phrasen, Stimmen, Partituren) als Liste der jeweils darunter liegenden Datenstruktur ausgeben, über diese iterieren und im funktionalen Stil manipulieren. {5}
- [x] beliebige MIDI-Nachrichten (z. B. noteOn, noteOff) an MIDI-Geräte (auch den integrierten MIDI-Synthesizer!) senden und empfangen _(siehe MidiIn/Out). {4}_
- [x] Mithilfe von „parallelen“ Listen Noten zu Phrasen hinzufügen. {4}
- [x] Mithilfe von verschachtelten Listen Akkorde zu Phrasen hinzufügen. {4}
- [x] Musikdaten (Noten, Phrasen, Part, Scores) als MIDI-Dateien exportieren. {3}

## Niedrige Priorität (optional)

Das System sollte...

- [x] [PlayCode](https://jythonmusic.me/play-code/) {5}
- [x] [AudioSample](https://jythonmusic.me/api/audiosample/) {4}
- [ ] [MidiSequence](https://jythonmusic.me/api/midisequence/) {4}
- [ ] [ModFunctions](https://jythonmusic.me/api/music-library-functions/mod-functions/) ist nicht das meiste davon recht simpel, funktional selbst zu implementieren? {3}
    - check functions for useful material that is not easily implemented
- [ ] mit OSC-fähigen Geräten kommunizieren _(siehe OSCIn/Out). {2}_
- [ ] MIDI-Datei als Score importieren. {1}
- [ ] [Metronome](https://jythonmusic.me/metronome/) {1}

# Nichtfunktionale Anforderungen

- [x] Die Bibliothek muss einfach zu verwenden & aufzusetzen sein.
- [x] Die Auswahl eines MIDI-Gerätes (MidiIn, MidiOut) muss für Laien einfach vorzunehmen sein (z. B. durch Dialog)
- [ ] Die Bibliothek muss effektiv mit den Event-Handlern einer GUI-Bibliothek (z. B. tkinter) verknüpfbar sein. \[thin layer für tkinter\]
- [x] Die Bibliothek muss sich am MIDI-Standard (1.0) orientieren.
- [x] Die verwendeten externen Bibliothek müssen maintained sein.
- [x] Die Schnittstellen müssen exakt dokumentiert sein und die Dokumentation muss IDE-integriert sowie als PDF oder HTML vorliegen (z. B. pydocs).
