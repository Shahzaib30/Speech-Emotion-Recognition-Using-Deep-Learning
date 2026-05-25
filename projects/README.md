# Projects — Speech Emotion Recognition

This folder contains runnable scripts for preprocessing and model training.

Scripts

- `preprocess_audio.py`: scans a directory for audio files and writes a CSV summary (`audio_summary.csv`).
- `train_audio_model.py`: a training template to be adapted for real models.

Usage examples

```bash
python projects/preprocess_audio.py --data-dir . --output-dir outputs
python projects/train_audio_model.py --data-dir data --output-dir outputs
```
