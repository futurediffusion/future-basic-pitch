from typing import List, Tuple, Optional

import pretty_midi


ChordEvent = Tuple[float, str]


CHORD_TEMPLATES = {
    (0, 4, 7): "major",
    (0, 3, 7): "minor",
    (0, 4, 7, 10): "7",
    (0, 3, 7, 10): "m7",
    (0, 4, 7, 11): "maj7",
    (0, 3, 6): "dim",
    (0, 4, 8): "aug",
}


def _classify_chord(pitch_classes: List[int]) -> Optional[str]:
    """Return a chord name for the given pitch classes if recognized."""
    pitch_classes = sorted(set(pitch_classes))
    for root in pitch_classes:
        intervals = tuple(sorted(((pc - root) % 12 for pc in pitch_classes)))
        for template, name in CHORD_TEMPLATES.items():
            if intervals == template:
                root_name = pretty_midi.note_number_to_name(root + 60)[:-1]
                if name == "major":
                    return f"{root_name} major"
                if name == "minor":
                    return f"{root_name} minor"
                return f"{root_name}{name}"
    return None


def detect_chords_from_midi(midi_path: str) -> List[ChordEvent]:
    """Estimate a simple chord progression from a MIDI file.

    This function groups active notes between onset/offset boundaries and
    matches the resulting pitch classes to a small set of chord templates.
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
    pm = pretty_midi.PrettyMIDI(midi_path)
    notes = [n for inst in pm.instruments for n in inst.notes]
    if not notes:
        return []

    times = sorted(set([n.start for n in notes] + [n.end for n in notes]))
    progression: List[ChordEvent] = []
    for i in range(len(times) - 1):
        t = times[i]
        active = [n for n in notes if n.start <= t < n.end]
        if len(active) < 2:
            continue
        pcs = [n.pitch % 12 for n in active]
        name = _classify_chord(pcs)
        if not name:
            continue
        if not progression or progression[-1][1] != name:
            progression.append((t, name))

    return progression
