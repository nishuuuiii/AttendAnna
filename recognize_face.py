import cv2
import csv
from datetime import datetime
import os
import time
from deepface import DeepFace

known_dir = "registered_faces"
cap = cv2.VideoCapture(0)
print("Camera on. Q dabao band karne ke liye")

frame_count = 0
present_since = {}  
attendance_marked = set()  
THRESHOLD_SECONDS = 15  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(frame, (320, 240))
    frame_count += 1

    if frame_count % 40 == 0:
        cv2.imwrite("temp_frame.jpg", small_frame)
        matched_name = "Unknown"

        for file in os.listdir(known_dir):
            try:
                result = DeepFace.verify(
                    img1_path="temp_frame.jpg",
                    img2_path=os.path.join(known_dir, file),
                    model_name="Facenet",
                    detector_backend="mtcnn",
                    enforce_detection=False,
                    distance_metric="cosine"
                )
                if result["verified"] and result["distance"] < (result["threshold"] * 0.85):
                    matched_name = file.replace(".jpg", "")
                    break
            except Exception:
                pass

        now = time.time()

        if matched_name != "Unknown":
            if matched_name not in present_since:
                present_since[matched_name] = now
                print(f"{matched_name} detected, timer started")

            elapsed = now - present_since[matched_name]

            if elapsed >= THRESHOLD_SECONDS and matched_name not in attendance_marked:
                attendance_marked.add(matched_name)
                file_exists = os.path.exists("attendance.csv")
                with open("attendance.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Name_RollNo", "Time"])
                    writer.writerow([matched_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                print(f"✅ ATTENDANCE MARKED: {matched_name}")
            else:
                print(f"{matched_name} present for {int(elapsed)}s")

            # Baaki sab ke timers reset karo, sirf current match ka rakho
            for other_name in list(present_since.keys()):
                if other_name != matched_name:
                    del present_since[other_name]
        else:
            # Koi detect nahi hua, sab timers reset
            present_since.clear()

        cv2.putText(frame, f"Detected: {matched_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Recognition - Q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nFinal Attendance:", attendance_marked)