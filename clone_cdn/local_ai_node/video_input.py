"""Video capture and processing module."""

import logging
from pathlib import Path
import cv2

logger = logging.getLogger(__name__)


def capture_frames(source: str = "0"):
    """Capture frames from camera or RTSP stream."""
    logger.debug("Opening video source %s", source)
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
        logger.error("Unable to open video source %s", source)
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame


def analyze_frame(frame) -> dict:
    """Analyze the video frame for facial expressions."""
    logger.debug("Analyzing frame")
    # Placeholder analysis; replace with mediapipe/ML model
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = []
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    detected = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in detected:
        faces.append({"box": [int(x), int(y), int(w), int(h)]})
    logger.debug("Detected faces: %s", faces)
    return {"faces": faces}
