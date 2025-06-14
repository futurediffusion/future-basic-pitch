import argparse
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.key_detection import detect_key_from_note_events


def main():
    parser = argparse.ArgumentParser(description="Detect key of a melody")
    parser.add_argument("audio_path", help="Path to the audio file")
    args = parser.parse_args()

    _, _, note_events = predict(
        args.audio_path,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
    )

    key = detect_key_from_note_events(note_events)
    if key is None:
        print("Could not detect key")
    else:
        print(f"Detected key: {key}")


if __name__ == "__main__":
    main()
