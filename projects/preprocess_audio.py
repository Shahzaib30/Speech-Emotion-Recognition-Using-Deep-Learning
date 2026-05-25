"""Quick audio dataset inspection and summary writer.

Scans a data directory for common audio file types and writes a small CSV
summary containing path, duration, and sample rate. Safe to run on large
folders (reads header info only when possible via `soundfile`).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

try:
    import soundfile as sf
    _HAS_SOUNDFILE = True
except Exception:
    _HAS_SOUNDFILE = False
import pandas as pd
import wave
import contextlib
try:
    import librosa
    _HAS_LIBROSA = True
except Exception:
    _HAS_LIBROSA = False


def list_audio_files(data_dir: Path) -> List[Path]:
    exts = {".wav", ".flac", ".mp3", ".ogg"}
    return [p for p in data_dir.rglob("*") if p.suffix.lower() in exts]


def inspect_audio(paths: List[Path]) -> pd.DataFrame:
    records = []
    for p in paths:
        try:
            if _HAS_SOUNDFILE:
                with sf.SoundFile(str(p)) as f:
                    duration = len(f) / f.samplerate
                    records.append({"path": str(p), "samplerate": f.samplerate, "duration_s": duration})
            else:
                if _HAS_LIBROSA:
                    y, sr = librosa.load(str(p), sr=None)
                    duration = len(y) / sr if sr else 0.0
                    records.append({"path": str(p), "samplerate": sr, "duration_s": duration})
                else:
                    # final fallback for WAV files using the stdlib wave module
                    try:
                        with contextlib.closing(wave.open(str(p), "r")) as wf:
                            frames = wf.getnframes()
                            sr = wf.getframerate()
                            duration = frames / float(sr) if sr else 0.0
                            records.append({"path": str(p), "samplerate": sr, "duration_s": duration})
                    except Exception:
                        continue
        except Exception:
            continue
    return pd.DataFrame.from_records(records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect audio dataset and write a CSV summary.")
    parser.add_argument("--data-dir", default=".", help="Directory containing audio files")
    parser.add_argument("--output-dir", default="outputs", help="Directory to write the summary CSV")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return

    audio_files = list_audio_files(data_dir)
    print(f"Found {len(audio_files)} audio files in {data_dir}")

    if audio_files:
        df = inspect_audio(audio_files)
        if not df.empty:
            df.to_csv(out_dir / "audio_summary.csv", index=False)
            print(f"Wrote audio summary to: {out_dir / 'audio_summary.csv'}")


if __name__ == "__main__":
    main()
