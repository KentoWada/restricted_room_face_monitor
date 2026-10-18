import cv2

SOURCE=0

cap = cv2.VideoCapture(SOURCE)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    cv2.imshow("Prototype", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
