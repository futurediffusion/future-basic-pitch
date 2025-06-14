import gradio as gr
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.note_creation import sonify_midi
from basic_pitch.key_detection import detect_key_from_note_events
import pretty_midi
import os
import tempfile


def transcribir(audio):
    tmpdir = tempfile.mkdtemp()
    _, midi_data, note_events = predict(
        audio,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
    )
    midi = os.path.join(
        tmpdir,
        os.path.splitext(os.path.basename(audio))[0] + "_basic_pitch.mid",
    )
    midi_data.write(midi)
    wav = os.path.join(
        tmpdir,
        os.path.splitext(os.path.basename(audio))[0] + "_basic_pitch.wav",
    )
    sonify_midi(midi_data, wav, sr=44100)
    key = detect_key_from_note_events(note_events)
    return midi, wav, (key or "No se pudo detectar la tonalidad")


def previsualizar_midi(midi_file):
    pm = pretty_midi.PrettyMIDI(midi_file)
    audio = pm.synthesize(44100)
    return 44100, audio


interface_transcribir = gr.Interface(
    fn=transcribir,
    inputs=gr.Audio(type="filepath"),
    outputs=[
        gr.File(label="MIDI"),
        gr.Audio(label="Preview"),
        gr.Textbox(label="Tonalidad"),
    ],
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
