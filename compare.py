from detector import load_model, detect_faces
from pathlib import Path

import cv2
import numpy as np

THRESHOLD = 0.47

IMG_DIR = Path("images")
app = load_model()

def embedding_of(path):

    image = cv2.imread(str(path))
    if image is None:
        raise SystemExit(f"Could not read {path}")

    faces = detect_faces(app, image)
    if len(faces) != 1:
        raise SystemExit(f"{path}: expected 1 face, found {len(faces)}")
    return faces[0].normed_embedding


a = embedding_of(IMG_DIR / "me0.jpg")
b = embedding_of(IMG_DIR/ "me1.jpg")
c = embedding_of(IMG_DIR / "me2.jpg")
d = embedding_of(IMG_DIR / "dta.jpg")

ENROLLED = {}
ENROLLED['Director'] = [a, b, c]

for name, embedding in ENROLLED.items():
    for e in embedding:
        print(name, np.dot(e, d))
