import argparse

import time

import cv2

from alerts import UnknownFaceAlert
from detector import detect_faces, load_model
from enroller import build_enrolled
from grab_frame import frames
from recognizer import best_match

SOURCE = 0  # later: an RTSP URL
PROCESS_EVERY = 3  # run the detector on every 3rd frame


def draw(frame, faces, labels, fps):
    for face, (name, score) in zip(faces, labels):
        x1, y1, x2, y2 = face.bbox.astype(int)
        color = (0, 0, 255) if name == "Unknown" else (0, 255, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{name} {score:.2f}", (x1, max(y1 - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, f"Faces: {len(faces)}  FPS: {fps:.1f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)


def main():
    parser = argparse.ArgumentParser(
        description="Live face recognition with audio alerts")

    parser.add_argument("--camera", type=int, default=SOURCE,
                        help="Webcam index(default: 0)")

    parser.add_argument("--mute", action="store_true",
                        help="Disable unknown-face audio alerts")

    args = parser.parse_args()

    audio_alert = UnknownFaceAlert(cooldown_seconds=10, enabled=not args.mute)

    app = load_model()
    enrolled = build_enrolled(app)
    if not enrolled:
        raise SystemExit("no enrolled people found in images/")
    faces = []
    labels = []
    prev = time.time()
    for i, frame in enumerate(frames(SOURCE)):
        if i % PROCESS_EVERY == 0:
            faces = detect_faces(app, frame)
            labels = [best_match(f.normed_embedding, enrolled) for f in faces]
            for name, score in labels:
                audio_alert.notify(name)
        now = time.time()
        fps = 1.0 / max(now - prev, 1e-6)
        prev = now
        draw(frame, faces, labels, fps)
        cv2.imshow("Prototype", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
