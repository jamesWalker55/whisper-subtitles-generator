import argparse
from pathlib import Path
import sys
import whisper


def format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    if hours > 0:
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    else:
        return f"{hours}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def create_partial_vtt(segment: dict):
    # float values in seconds
    start = format_timestamp(segment["start"])
    end = format_timestamp(segment["end"])
    # replace '-->' arrows, because they have special meanings in the vtt format
    text = segment["text"].replace("-->", "->").strip()
    return f"{start} --> {end}\n{text}"


def create_vtt(segments: list[dict]):
    contents = "\n\n".join(create_partial_vtt(s) for s in segments)
    return f"WEBVTT\n\n{contents}"


def get_boolean_choice(default: bool = False):
    assert default in (True, False), "Expected default choice to be a boolean"

    choice = None

    while (choice is not True) or (choice is not False):
        choice = input("  > ").strip().lower()
        if choice in ("y", "n", ""):
            if choice == "":
                return default

            return choice == "y"

        print("    Please input either 'y' or 'n'")


def main():
    parser = argparse.ArgumentParser(description="Create subtitles from a file.")
    parser.add_argument(
        "input",
        type=Path,
        help="the input file to generate subtitles from",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="the path to save the subtitles, defaults to the original path with a `.vtt` extension",
    )
    parser.add_argument(
        "--model",
        "-m",
        choices=whisper.available_models(),
        default="small.en",
        help="the model to use, defaults to 'small.en'",
    )
    parser.add_argument(
        "--skip-confirmation",
        "-y",
        action="store_true",
        help="if the output file already exists, this will skip the confirmation prompt",
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.input.with_suffix(".vtt")

    print(f"Generating subtitles from: {args.input}")
    print(f"Subtitles will be saved to: {args.output}")
    print()

    if args.output.exists() and not args.skip_confirmation:
        print(f"The output path already exists: {args.output.resolve()}")
        print(f"Do you want to overwrite it? (y/N)")

        if not get_boolean_choice():
            sys.exit()

    model = whisper.load_model(args.model)

    result = model.transcribe(
        str(args.input),
        verbose=True,
        language="English",
    )

    vtt_contents = create_vtt(result["segments"])
    with open(str(args.output), "w", encoding="utf8") as f:
        f.write(vtt_contents)


if __name__ == "__main__":
    main()
