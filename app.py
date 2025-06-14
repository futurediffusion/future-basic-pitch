import argparse
import gradio as gr
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import pretty_midi
import os
import tempfile


parser = argparse.ArgumentParser(description="Basic Pitch Gradio app")
parser.add_argument("--onset-threshold", type=float, default=0.6)
parser.add_argument("--frame-threshold", type=float, default=0.4)
parser.add_argument("--minimum-note-length", type=float, default=200.0)
parser.add_argument("--minimum-frequency", type=float, default=55.0)
parser.add_argument("--maximum-frequency", type=float, default=1760.0)
parser.add_argument("--multiple-pitch-bends", action="store_true")
parser.add_argument("--no-melodia", action="store_true")
args = parser.parse_args()


def transcribir(audio):
    tmpdir = tempfile.mkdtemp()
    predict_and_save(
        [audio],
        tmpdir,
        save_midi=True,
        sonify_midi=True,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
        onset_threshold=args.onset_threshold,
        frame_threshold=args.frame_threshold,
        minimum_note_length=args.minimum_note_length,
        minimum_frequency=args.minimum_frequency,
        maximum_frequency=args.maximum_frequency,
        multiple_pitch_bends=args.multiple_pitch_bends,
        melodia_trick=not args.no_melodia,
    )
    midi = os.path.join(
        tmpdir,
        os.path.splitext(os.path.basename(audio))[0] + "_basic_pitch.mid",
    )
    wav = os.path.join(
        tmpdir,
        os.path.splitext(os.path.basename(audio))[0] + "_basic_pitch.wav",
    )
    return midi, wav


def previsualizar_midi(midi_file):
    pm = pretty_midi.PrettyMIDI(midi_file)
    audio = pm.synthesize(44100)
    return 44100, audio


interface_transcribir = gr.Interface(
    fn=transcribir,
    inputs=gr.Audio(type="filepath"),
    outputs=[gr.File(label="MIDI"), gr.Audio(label="Preview")],
)

interface_preview = gr.Interface(
    fn=previsualizar_midi,
    inputs=gr.File(type="filepath", label="MIDI file"),
    outputs=gr.Audio(label="Preview"),
)

gr.TabbedInterface(
    [interface_transcribir, interface_preview],
    ["Transcribir Audio", "Previsualizar MIDI"],
).launch()
