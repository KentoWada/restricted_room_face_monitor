import cv2
import time

def open_camera(source=0):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video source: {source}")
    return cap


def frames(source=0, reconnect=True, rety_delay=2.0):
    """Yield frames one by one until the source ends."""
    cap = open_camera(source)
    try:
        while True:
            ok, frame = cap.read()
            if ok:
                yield frame
                continue
            cap.release()

            if not reconnect:
                break

            while True:
                time.sleep(retry_delay)
                cap.cv2.VideoCapture(source)

                if cap.isOpened():
                    break
    finally:
        cap.release()


def main():
    for frame in frames(0):
        cv2.imshow("Prototype", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
