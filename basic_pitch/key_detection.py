import numpy as np
import pretty_midi
from typing import List, Tuple, Optional

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

NoteEvent = Tuple[float, float, int, float, Optional[List[int]]]

def _pitch_class_distribution(note_events: List[NoteEvent]) -> np.ndarray:
    """Return duration weighted pitch class distribution."""
    pc = np.zeros(12)
    for start, end, pitch, _amp, _pb in note_events:
        duration = max(0.0, end - start)
        pc[pitch % 12] += duration
    return pc

def detect_key_from_note_events(note_events: List[NoteEvent]) -> Optional[str]:
    """Estimate key from note events using a simple Krumhansl-Schmuckler profile."""
    pc = _pitch_class_distribution(note_events)
    if pc.sum() == 0:
        return None
    pc = pc / np.linalg.norm(pc)
    best_score = -np.inf
    best_key = None
    for tonic in range(12):
        prof = np.roll(MAJOR_PROFILE, tonic)
        score = np.dot(pc, prof / np.linalg.norm(prof))
        if score > best_score:
            best_score = score
            best_key = (tonic, "major")
    for tonic in range(12):
        prof = np.roll(MINOR_PROFILE, tonic)
        score = np.dot(pc, prof / np.linalg.norm(prof))
        if score > best_score:
            best_score = score
            best_key = (tonic, "minor")
    tonic_name = pretty_midi.note_number_to_name(60 + best_key[0])[:-1]
    return f"{tonic_name} {best_key[1]}"
