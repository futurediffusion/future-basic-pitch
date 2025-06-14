import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

import importlib.util

spec = importlib.util.spec_from_file_location(
    "chord_detection", os.path.join(ROOT, "basic_pitch", "chord_detection.py")
)
chord_detection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chord_detection)
detect_chords_from_midi = chord_detection.detect_chords_from_midi
import pretty_midi


def test_detect_chords_simple():
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(0)
    inst.notes.append(pretty_midi.Note(velocity=100, pitch=60, start=0.0, end=1.0))
    inst.notes.append(pretty_midi.Note(velocity=100, pitch=64, start=0.0, end=1.0))
    inst.notes.append(pretty_midi.Note(velocity=100, pitch=67, start=0.0, end=1.0))
    pm.instruments.append(inst)
    tmp = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
    pm.write(tmp.name)
    tmp.close()
    chords = detect_chords_from_midi(tmp.name)
    assert chords and 'C' in chords[0][1]
