from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

def generate_study_schedule(subjects, daily_hours, exam_date):
    try:
        exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
        today = datetime.today().date()
        days_left = (exam_date - today).days - 1  # Exclude exam day

        if days_left <= 0:
            return {"error": "Exam date must be in the future."}

        timetable = []
        study_hours = int(daily_hours)

        for day in range(1, days_left + 1):  # Stop one day before exam
            schedule = []
            hours_allocated = 0
            random.shuffle(subjects)

            while hours_allocated < study_hours:
                for subject in subjects:
                    if hours_allocated >= study_hours:
                        break  # Stop once daily hours are reached
                    session_hours = min(study_hours - hours_allocated, max(1, study_hours // len(subjects)))
                    schedule.append({"subject": subject, "duration": f"{session_hours} hrs"})
                    hours_allocated += session_hours

            timetable.append({"day": f"Day {day}", "schedule": schedule})

        return timetable

    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return "✅ Flask server is running! Use the /generate_ai_timetable API."

@app.route("/generate_ai_timetable", methods=["POST"])
def generate_ai_timetable():
    try:
        data = request.get_json()
        
        subjects = data.get("subjects")
        daily_hours = data.get("daily_hours")
        exam_date = data.get("exam_date")
        
        if not subjects or not daily_hours or not exam_date:
            return jsonify({"error": "Missing required fields"}), 400
        
        timetable = generate_study_schedule(subjects, daily_hours, exam_date)
        return jsonify({"timetable": timetable})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
