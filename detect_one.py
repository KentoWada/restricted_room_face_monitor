import cv2
from insightface.app import FaceAnalysis


def load_model(det_size=(640, 640)):
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=-1, det_size=det_size)
    return app


def detect_faces(app, frame):
    return app.get(frame)


def main():
    app = load_model()
    image = cv2.imread("test.jpg")
    if image is None:
        raise SystemExit("test.jpg not found")
    print(len(detect_faces(app, image)))


if __name__ == "__main__":
    main()
