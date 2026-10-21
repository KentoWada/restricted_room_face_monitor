from pathlib import Path
import cv2

IMAGE_DIR = Path('images')
IMAGE_DIR.mkdir(exist_ok=True)


def ask_name():
    while True:
        name = input("What is your name ?: ").strip().lower()
        if name and name.replace("-", "").replace("_", "").isalnum():
            return name
        print("Use letters and numbers only. Underscores and Hyphens are useable.")


# Asks for the number of images you would like to take
def ask_count():
    while True:
        text = input("How many pictures ?: ")
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Please enter a whole number above 0.")

NUM_OF_IMAGES = ask_count()
COUNTER = 0


def next_path(person_dir):
    n = len(list(person_dir.glob("*.jpg")))
    while (person_dir / f"{n}.jpg").exists():
        n += 1
    return  person_dir / f"{n}.jpg"

NAME = ask_name()
PERSON_DIR = IMAGE_DIR / NAME
PERSON_DIR.mkdir(parents=True, exist_ok=True)

cam = cv2.VideoCapture(0)

# Loop for taking images.
while COUNTER < NUM_OF_IMAGES:
    ok, frame = cam.read()
    if not ok:
        break

    display = frame.copy()
    cv2.putText(display, "S: Take picture   Q: Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(display, f"Saved {COUNTER} of {NUM_OF_IMAGES}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Enroll", display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("s"):
        saved = cv2.imwrite(str(next_path(PERSON_DIR)), frame)
        if saved:
            COUNTER += 1
        else:
            print("Could not save the picture.")

cam.release()
cv2.destroyAllWindows()
