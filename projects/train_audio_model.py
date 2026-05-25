"""Training template for audio classification models (placeholder).

This script is a starting point for building a training loop for SER models.
Replace the placeholder model and dataset code with your project's specifics.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an audio classification model (template)")
    parser.add_argument("--data-dir", default="data", help="Dataset folder")
    parser.add_argument("--output-dir", default="outputs", help="Where to save checkpoints")
    parser.add_argument("--epochs", type=int, default=10)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return

    print("This is a training template. Plug in dataset, model, optimizer, and training loop.")


if __name__ == "__main__":
    main()
