from pathlib import Path
from detect_one import load_model, detect_faces

import cv2

IMAGE_DIR = Path("images")
EXTENSIONS = {".jpg", ".jpeg", ".png"}


def embedding_from_file(app, path):
    image = cv2.imread(str(path))
    if image is None:
        print(f"skipping {path}: could not read")
        return None
    faces = detect_faces(app, image)
    if len(faces) != 1:
        print(f"skipping {path}: expected 1 face, found {len(faces)}")
        return None
    return faces[0].normed_embedding


def build_enrolled(app, image_dir=IMAGE_DIR):
    enrolled = {}
    for person_dir in sorted(image_dir.iterdir()):
        if not person_dir.is_dir():
            continue
        embeddings = []
        for path in sorted(person_dir.iterdir()):
            if path.suffix.lower() not in EXTENSIONS:
                continue
            e = embedding_from_file(app, path)
            if e is not None:
                embeddings.append(e)
        if embeddings:
            enrolled[person_dir.name] = embeddings
    return enrolled


def main():
    app = load_model()
    enrolled = build_enrolled(app)
    for name, embeddings in enrolled.items():
        print(name, len(embeddings))


if __name__ == "__main__":
    main()
