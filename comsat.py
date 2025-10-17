# cgpa_gpa_tool_comsats.py
import streamlit as st
import pandas as pd

# ------------------------------
# COMSATS Grade Conversion Function
# ------------------------------
def marks_to_grade_points(score):
    if score >= 85:
        return 4.00, "A"
    elif score >= 80:
        return 3.67, "A–"
    elif score >= 75:
        return 3.33, "B+"
    elif score >= 70:
        return 3.00, "B"
    elif score >= 65:
        return 2.67, "B–"
    elif score >= 60:
        return 2.33, "C+"
    elif score >= 55:
        return 2.00, "C"
    elif score >= 50:
        return 1.67, "C–"
    else:
        return 0.00, "F"

# ------------------------------
# Function to Compute GPA
# ------------------------------
def gpa_calculator(marks, credits):
    total_quality_points = 0
    total_credit_hours = 0
    subjects_summary = []

    for m, ch in zip(marks, credits):
        g_points, letter = marks_to_grade_points(m)
        total_quality_points += g_points * ch
        total_credit_hours += ch
        subjects_summary.append({
            "Obtained Marks": m,
            "Credit Hours": ch,
            "Letter Grade": letter,
            "Grade Point": g_points
        })

    gpa = round(total_quality_points / total_credit_hours, 2) if total_credit_hours else 0
    return gpa, subjects_summary

# ------------------------------
# Streamlit Web App UI
# ------------------------------
st.set_page_config(page_title="COMSATS GPA-CGPA Estimator", layout="wide")

st.title("🎓 COMSATS GPA & CGPA Estimator")
st.markdown("Easily calculate *semester GPA* and *overall CGPA* based on the official COMSATS grading system.")

# Step 1: Ask for number of semesters
semesters = st.number_input("How many semesters have you completed?", min_value=1, step=1)

results = []  # store GPAs and credits of each semester

# Step 2: Enter data for each semester
for s in range(1, semesters + 1):
    st.markdown(f"### 📘 Semester {s} Details")
    total_subjects = st.number_input(f"Subjects in Semester {s}:", min_value=1, step=1, key=f"subjects_{s}")

    marks_data, credit_data = [], []

    for subj in range(1, total_subjects + 1):
        col1, col2 = st.columns(2)
        with col1:
            marks = st.number_input(f"Marks for Subject {subj}", 0, 100, key=f"marks_{s}_{subj}")
        with col2:
            credit = st.number_input(f"Credit Hours for Subject {subj}", 1.0, 5.0, 3.0, 0.5, key=f"credit_{s}_{subj}")
        marks_data.append(marks)
        credit_data.append(credit)

    if st.button(f"Compute GPA for Semester {s}", key=f"calc_gpa_{s}"):
        sem_gpa, summary = gpa_calculator(marks_data, credit_data)
        results.append({"gpa": sem_gpa, "credits": sum(credit_data)})

        df = pd.DataFrame(summary)
        st.subheader(f"📋 Subject Grade Breakdown (Semester {s})")
        st.dataframe(df, use_container_width=True)

        st.success(f"✅ GPA for Semester {s}: *{sem_gpa}*")

# Step 3: Final CGPA Computation
if len(results) > 0:
    total_qp = sum(item["gpa"] * item["credits"] for item in results)
    total_ch = sum(item["credits"] for item in results)
    cgpa = round(total_qp / total_ch, 2)

    st.markdown("---")
    st.header(f"🏅 Overall CGPA (Till Current Semester): *{cgpa}*")

    if cgpa >= 3.5:
        status = "Distinction"
    elif cgpa >= 3.0:
        status = "First Division"
    elif cgpa >= 2.5:
        status = "Second Division"
    elif cgpa >= 2.0:
        status = "Pass"
    else:
        status = "Fail"

    st.info(f"🎯 Academic Standing: *{status}*")
