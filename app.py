import gradio as gr
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
import os
import tempfile


def transcribir(audio):
    tmpdir = tempfile.mkdtemp()
    predict_and_save(
        [audio],
        tmpdir,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
    )
    midi = os.path.join(
        tmpdir,
        os.path.splitext(os.path.basename(audio))[0] + "_basic_pitch.mid",
    )
    return midi


gr.Interface(fn=transcribir, inputs=gr.Audio(type="filepath"), outputs=gr.File()).launch()
