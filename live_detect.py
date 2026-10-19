import time

import cv2
from insightface.app import FaceAnalysis

# 0 = laptop webcam.will later, swap for an RTSP URL, e.g. "rtsp://user:pass@192.168.1.10:554/stream"
SOURCE = 0
DET_SIZE = (640, 640)
PROCESS_EVERY = 3  # run the detector on every 3rd frame so CPU-only laptops keep up

# Load the model once
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=-1, det_size=DET_SIZE)

cap = cv2.VideoCapture(SOURCE)
if not cap.isOpened():
    raise SystemExit(f"Could not open video source: {SOURCE}")

frame_count = 0
faces = []  # last known detections, reused on frames we skip
prev_time = time.time()

while True:
    ok, frame = cap.read()
    if not ok:
        print("No frame received, stopping.")
        break

    # Only run the heavy detector every Nth frame
    if frame_count % PROCESS_EVERY == 0:
        faces = app.get(frame)
    frame_count += 1

    # Draw a box and confidence score around each face
    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{face.det_score:.2f}", (x1, max(y1 - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # FPS and face count overlay
    now = time.time()
    fps = 1.0 / max(now - prev_time, 1e-6)
    prev_time = now
    cv2.putText(frame, f"Faces: {len(faces)}  FPS: {fps:.1f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Prototype", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
