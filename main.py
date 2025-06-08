from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

GRADE_TO_SCORE = {
    "A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class StudentInput(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

@app.post("/score", response_model=StudentSummary)
def calculate_gpa(data: StudentInput):
    total_score = 0.0
    total_credits = 0
    for course in data.courses:
        if course.grade not in GRADE_TO_SCORE:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        score = GRADE_TO_SCORE[course.grade]
        total_score += score * course.credits
        total_credits += course.credits
    gpa = round(total_score / total_credits, 3) if total_credits > 0 else 0.0
    return {
        "student_id": data.student_id,
        "name": data.name,
        "gpa": gpa,
        "total_credits": total_credits
    }
