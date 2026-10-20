from detect_one import load_model, detect_faces
from pathlib import Path

import cv2
import numpy as np

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


a = embedding_of(IMG_DIR / ".jpg")
b = embedding_of(IMG_DIR/ ".jpg")
c = embedding_of(IMG_DIR / ".jpg")

print("same person:", np.dot(a, c))
print("different person:", np.dot(a, c))
