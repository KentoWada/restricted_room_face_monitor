import cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=-1, det_size=(640,640))

frames = cv2.imread("test.jpg")
faces = app.get(frames)

print(len(faces))
