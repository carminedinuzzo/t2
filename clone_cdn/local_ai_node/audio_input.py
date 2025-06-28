"""Audio input and transcription module."""

import logging
import subprocess
from pathlib import Path

CONFIG = {
    "audio_device": "default",
    "model": "base.en",
}

logger = logging.getLogger(__name__)


def record_audio(temp_path: Path) -> Path:
    """Record audio from the configured device and save to a temporary file."""
    logger.debug("Recording audio to %s", temp_path)
    # Placeholder using `arecord` for simplicity
    cmd = [
        "arecord",
        "-d",
        "5",
        "-f",
        "cd",
        str(temp_path),
    ]
    subprocess.run(cmd, check=False)
    return temp_path


def transcribe(audio_path: Path) -> str:
    """Transcribe the recorded audio using whisper.cpp."""
    logger.debug("Transcribing %s", audio_path)
    result = subprocess.run(
        ["./main", "-m", CONFIG["model"], "-f", str(audio_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    transcript = result.stdout.strip()
    logger.debug("Transcript: %s", transcript)
    return transcript
