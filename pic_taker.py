from pathlib import Path
import cv2

IMAGE_DIR = Path('images')
IMAGE_DIR.mkdir(exist_ok=True)

NUM_OF_IMAGES = 2
COUNTER = 0

cam = cv2.VideoCapture(0)

while COUNTER < NUM_OF_IMAGES:
    ok, frame = cam.read()
    if not ok:
        break

    cv2.imshow("Me", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("s"):
        cv2.imwrite(str(IMAGE_DIR/f"me{COUNTER}.jpg"), frame)
        COUNTER += 1

cam.release()
cv2.destroyAllWindows()
