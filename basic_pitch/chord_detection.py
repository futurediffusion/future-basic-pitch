import tempfile
from typing import List, Tuple

from music21 import converter, chord


ChordEvent = Tuple[float, str]


def detect_chords_from_midi(midi_path: str) -> List[ChordEvent]:
    """Estimate a simple chord progression from a MIDI file.

    This function uses :mod:`music21` to chordify the MIDI data and extracts
    the name of each chord along with its offset time in seconds.
    Chords with fewer than two pitches are ignored.

    Parameters
    ----------
    midi_path: str
        Path to a MIDI file.

    Returns
    -------
    List[ChordEvent]
        A list of ``(time, chord_name)`` tuples.
    """
    score = converter.parse(midi_path)
    chordified = score.chordify()
    progression: List[ChordEvent] = []
    for c in chordified.flat.getElementsByClass(chord.Chord):
        if len(c.pitches) < 2:
            continue
        name = c.pitchedCommonName or c.commonName or "unknown"
        progression.append((float(c.offset), name))
    return progression
