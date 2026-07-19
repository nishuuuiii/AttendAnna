import csv
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CSV se attendance data padho
attendance_data = []
with open("attendance.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # header skip karo
    for row in reader:
        attendance_data.append(row)

if not attendance_data:
    print("Koi attendance data nahi mila.")
else:
    data_text = "\n".join([f"{row[0]} marked present at {row[1]}" for row in attendance_data])

    prompt = f"""Here is classroom attendance data:

{data_text}

Generate a short, clear summary (3-4 sentences) of the attendance for this lecture. Mention total students present and any notable patterns."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content
    print("\n--- AI Attendance Summary ---")
    print(summary)

    with open("summary.txt", "w") as f:
        f.write(summary)