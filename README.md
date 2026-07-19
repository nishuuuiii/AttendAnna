# AttendAnna — AI-Powered Classroom Attendance System

Built for the OpenAI x NamasteDev Hackathon.

## Problem
Traditional attendance systems only verify entry — students can check in and leave, making proxy attendance easy. There's no way to confirm a student was actually present throughout the lecture.

## Solution
AttendAnna uses AI-based face recognition to continuously verify a student's presence, not just their entry. A student registers their face once, and the system tracks how long they remain visible via camera. Attendance is only marked "Present" after a set duration of continuous detection — solving the "swipe in and leave" problem.

## How It Works
1. **Register** — Student's face is captured and saved with their name and roll number.
2. **Recognize** — Live camera feed is compared against registered faces using DeepFace (Facenet model).
3. **Timer-based marking** — If a face is detected consistently for a set threshold (e.g. 2-3 minutes), attendance is automatically logged.
4. **CSV logging** — Every marked attendance entry is saved with a timestamp.
5. **AI Summary** — Attendance data is sent to an LLM (Llama 3.3 70B via Groq) to generate a plain-English summary of the lecture's attendance.

## Tech Stack
- Python
- OpenCV — webcam access and frame processing
- DeepFace (Facenet model, MTCNN detector) — face recognition
- Groq API (Llama 3.3 70B) — AI-generated attendance summaries
- CSV — attendance logging

## Project Structure

webcam_test.py       # Basic webcam access test
register_face.py     # Face registration script
recognize_face.py    # Live recognition + timer-based attendance marking
generate_summary.py  # AI-generated attendance summary
app.py                # Streamlit UI (work in progress — core scripts above are the primary working demo)
attendance.csv        # Logged attendance records

## Running the Project
1. Clone the repo and create a virtual environment
2. Install dependencies
3. Add your Groq API key in a `.env` file:
4. Run individual scripts:
python register_face.py
python recognize_face.py
python generate_summary.py

OR 
(Optional — Streamlit UI is still being refined)
streamlit run app.py

## Future Scope
- Multi-face simultaneous detection for full classrooms
- Liveness/anti-spoofing detection to prevent photo-based spoofing
- Entry-scanner integration (thumb/face scan before class + continuous camera verification inside)
- Optimized face-encoding database for scaling to 50+ students
- Late arrival / early exit flagging

## Use Cases Beyond Classrooms
- Corporate offices (employee check-in)
- Coaching centers / tuitions
- Events and workshops
- Exam invigilation centers

## Team
Solo build — Nishanth Shetty (Team: AttendAnna)

