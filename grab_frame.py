import cv2

cap = cv2.VideoCapture(0)
ok, frame = cap.read()
print(ok, frame.shape)

cv2.imwrite("first_test_img.jpg", frame)
cap.release()
