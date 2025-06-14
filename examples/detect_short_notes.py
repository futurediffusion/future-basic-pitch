#!/usr/bin/env python
"""Example script to run Basic Pitch with thresholds tuned for short notes."""

import argparse
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe short percussive notes.")
    parser.add_argument("audio_path", help="Path to the input audio file")
    parser.add_argument("--output-midi", default=None, help="Optional output MIDI file")
    parser.add_argument("--onset-threshold", type=float, default=0.3)
    parser.add_argument("--frame-threshold", type=float, default=0.25)
    parser.add_argument("--minimum-note-length", type=float, default=40.0,
                        help="Minimum note length in milliseconds")
    args = parser.parse_args()

    model_output, midi_data, notes = predict(
        args.audio_path,
        ICASSP_2022_MODEL_PATH,
        onset_threshold=args.onset_threshold,
        frame_threshold=args.frame_threshold,
        minimum_note_length=args.minimum_note_length,
        melodia_trick=True,
    )

    print("Detected notes:")
    for start_time, end_time, pitch, amplitude, _ in notes:
        print(f"start={start_time:.3f} end={end_time:.3f} pitch={pitch} amplitude={amplitude:.3f}")

    if args.output_midi:
        midi_data.write(args.output_midi)
        print(f"MIDI saved to {args.output_midi}")


if __name__ == "__main__":
    main()
