import time
import cv2

from detector import detect_faces, load_model
from grab_frame import frames

SOURCE = 0  # later: an RTSP URL
PROCESS_EVERY = 3  # run the detector on every 3rd frame


def draw(frame, faces, fps):
    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{face.det_score:.2f}", (x1, max(y1 - 8, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(frame, f"Faces: {len(faces)}  FPS: {fps:.1f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)


def main():
    app = load_model()
    faces = []
    prev = time.time()
    for i, frame in enumerate(frames(SOURCE)):
        if i % PROCESS_EVERY == 0:
            faces = detect_faces(app, frame)
        now = time.time()
        fps = 1.0 / max(now - prev, 1e-6)
        prev = now
        draw(frame, faces, fps)
        cv2.imshow("Prototype", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
