import streamlit as st
import csv
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AttendAnna", layout="centered")
st.title("📋 AttendAnna — Smart Attendance System")

st.info("This hosted demo shows the attendance log and AI summary. Live face recognition runs locally (see demo video) due to camera/model requirements on cloud hosting.")

tab1, tab2 = st.tabs(["Attendance Log", "AI Summary"])

with tab1:
    st.header("Attendance Log")
    if os.path.exists("attendance.csv"):
        with open("attendance.csv", "r") as f:
            st.text(f.read())
    else:
        st.warning("No attendance data yet.")

with tab2:
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