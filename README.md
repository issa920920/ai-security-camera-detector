# AI Security Camera

Real-time car detection on a home IP camera. The script reads the camera's RTSP stream, runs YOLOv8 object detection and tracking on each frame, and sends a Telegram message when a new car pulls up.

## How it works

1. **Read the stream**: OpenCV pulls frames from a Reolink camera over RTSP.
2. **Detect and track**: YOLOv8 (`yolov8n`, pre-trained on COCO) finds objects in each frame. `model.track()` gives each object an ID that stays the same across frames.
3. **Alert once per car**: a car's ID is stored when it first appears, so you get one alert instead of one per frame. IDs not seen for 30 seconds are forgotten, so a car that leaves and comes back triggers a new alert.
4. **Notify**: alerts go to a Telegram bot.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill in your camera URL and Telegram details
python detect_cars.py
```

The YOLOv8 model downloads automatically on first run. Press `q` to quit.

To detect something else, set `TARGET_CLASS` in `.env` to any COCO class, such as `person` or `truck`.

## Tech

Python, OpenCV, Ultralytics YOLOv8, RTSP, Telegram Bot API

## Ideas you can build on top of this model

- Save a short video clip when an alert fires
- Support several cameras at once
