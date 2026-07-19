import cv2
import os

# Folder jahan registered faces save honge
if not os.path.exists("registered_faces"):
    os.makedirs("registered_faces")

name = input("Enter student name: ")
roll_no = input("Enter roll number: ")

cap = cv2.VideoCapture(0)
print("Camera khul raha hai... Photo lene ke liye SPACE dabao, cancel ke liye Q")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    cv2.imshow("Register Face - SPACE to capture, Q to quit", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):
        filename = f"registered_faces/{name}_{roll_no}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        break
    elif key == ord('q'):
        print("Cancelled")
        break

cap.release()
cv2.destroyAllWindows()