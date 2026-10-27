"""
AI Security Camera - car arrival alerts

Reads a live RTSP camera stream, detects and tracks cars with YOLOv8,
and sends a Telegram alert once per new car (not every frame).
"""
import os
import time

import cv2
from dotenv import load_dotenv
from ultralytics import YOLO

from telegramBot import sendAlert

load_dotenv()

RTSP_URL = os.environ["RTSP_URL"]          # set in .env, never hard-coded
TARGET_CLASS = os.getenv("TARGET_CLASS", "car")
COOLDOWN = int(os.getenv("COOLDOWN_SECONDS", "30"))

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(RTSP_URL)

seen_id = {}  # track_id -> last time it was seen

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # track() keeps the same ID on an object across frames
    results = model.track(frame, persist=True, verbose=False)
    frame = results[0].plot()
    now = time.time()

    for box in results[0].boxes:
        if model.names[int(box.cls)] != TARGET_CLASS:
            continue
        if box.id is None:
            continue
        track_id = int(box.id)

        # alert only the first time this tracked car appears
        if track_id not in seen_id:
            print(f"new {TARGET_CLASS} detected (id {track_id})")
            sendAlert(f"{TARGET_CLASS} pulled up")

        seen_id[track_id] = now

    # forget cars that haven't been seen for COOLDOWN seconds
    seen_id = {i: t for i, t in seen_id.items() if now - t < COOLDOWN}

    cv2.imshow("HomeCam", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
