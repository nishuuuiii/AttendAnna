import streamlit as st
import cv2
import os
import csv
import time
from datetime import datetime
from deepface import DeepFace
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

known_dir = "registered_faces"
if not os.path.exists(known_dir):
    os.makedirs(known_dir)

st.set_page_config(page_title="AttendAnna", layout="centered")
st.title("📋 AttendAnna — Smart Attendance System")

tab1, tab2, tab3 = st.tabs(["Register Student", "Take Attendance", "AI Summary"])

# TAB 1: REGISTER
with tab1:
    st.header("Register a New Student")
    name = st.text_input("Student Name")
    roll_no = st.text_input("Roll Number")
    photo = st.camera_input("Capture Face")

    if st.button("Save Registration"):
        if name and roll_no and photo:
            filename = f"{known_dir}/{name}_{roll_no}.jpg"
            with open(filename, "wb") as f:
                f.write(photo.getbuffer())
            st.success(f"Registered {name} (Roll No: {roll_no})")
        else:
            st.warning("Please fill name, roll number, and capture a photo.")

# TAB 2: TAKE ATTENDANCE
with tab2:
    st.header("Mark Attendance")
    check_photo = st.camera_input("Scan Face for Attendance")

    if st.button("Mark Present"):
        if check_photo:
            with open("temp_check.jpg", "wb") as f:
                f.write(check_photo.getbuffer())

            matched_name = "Unknown"
            for file in os.listdir(known_dir):
                try:
                    result = DeepFace.verify(
                        img1_path="temp_check.jpg",
                        img2_path=os.path.join(known_dir, file),
                        model_name="Facenet",
                        detector_backend="mtcnn",
                        enforce_detection=False,
                        distance_metric="cosine"
                    )
                    if result["verified"]:
                        matched_name = file.replace(".jpg", "")
                        break
                except Exception:
                    pass

            if matched_name != "Unknown":
                file_exists = os.path.exists("attendance.csv")
                with open("attendance.csv", "a", newline="") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["Name_RollNo", "Time"])
                    writer.writerow([matched_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                st.success(f"✅ Attendance marked for {matched_name}")
            else:
                st.error("Face not recognized. Please register first.")
        else:
            st.warning("Please capture a photo first.")

    if os.path.exists("attendance.csv"):
        st.subheader("Attendance Log")
        with open("attendance.csv", "r") as f:
            st.text(f.read())

# TAB 3: AI SUMMARY
with tab3:
    st.header("AI-Generated Attendance Summary")

    if st.button("Generate Summary"):
        if not os.path.exists("attendance.csv"):
            st.warning("No attendance data yet.")
        else:
            attendance_data = []
            with open("attendance.csv", "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    attendance_data.append(row)

            if not attendance_data:
                st.warning("No attendance data yet.")
            else:
                data_text = "\n".join([f"{row[0]} marked present at {row[1]}" for row in attendance_data])
                prompt = f"""Here is classroom attendance data:

{data_text}

Generate a short, clear summary (3-4 sentences) of the attendance for this lecture."""

                with st.spinner("Generating summary..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    summary = response.choices[0].message.content
                    st.success("Summary generated!")
                    st.write(summary)