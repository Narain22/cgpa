import streamlit as st
import math

# Define the custom grade points
grade_points = {
    "O": 10.0,
    "A+": 9.0,
    "A": 8.0,
    "B+": 7.0,
    "B": 6.0,
    "C": 5.0,
}

def calculate_required_grades(target_cgpa, current_cgpa, subjects):
    total_credits = 0
    weighted_grade_points = 0

    for subject, (credits, difficulty) in subjects.items():
        total_credits += credits
        weighted_grade_points += credits * grade_points.get("A", 0) * (1 + difficulty)  # Use default grade as "A"

    max_possible_cgpa = (current_cgpa * total_credits + weighted_grade_points) / total_credits
    target_cgpa = min(target_cgpa, 9.5)  # Cap target CGPA at 9.5
    
    dp = [0] * int(max_possible_cgpa * 100 + 1)  # DP table

    for grade, points in grade_points.items():
        for i in range(int(max_possible_cgpa * 100) - int(points * 100) + 1):
            dp[i + int(points * 100)] = max(dp[i + int(points * 100)], dp[i] + points)
    
    required_grades = {}
    for subject, (credits, difficulty) in subjects.items():
        required_grade_points = ((target_cgpa * total_credits) - weighted_grade_points + credits * dp[int(target_cgpa * 100) - int(current_cgpa * 100) + int(grade_points.get("A", 0) * 100)] * (1 + difficulty)) / (total_credits * target_cgpa)
        required_grade_points = math.ceil(required_grade_points)  # Round up to the nearest whole number
        required_grade = next((g for g, points in grade_points.items() if required_grade_points >= points), "C")  # Default to "C" if no grade found
        required_grades[subject] = required_grade
    
    return required_grades, target_cgpa

def main():
    st.title("CGPA Predictor App")
    
    st.write("Enter your current CGPA, target CGPA, and details of subjects:")

    current_cgpa = st.number_input("Current CGPA:", min_value=0.0, max_value=10.0, step=0.01)
    target_cgpa = st.number_input("Target CGPA:", min_value=0.0, max_value=10.0, step=0.01)

    num_subjects = st.number_input("Number of subjects:", min_value=1, max_value=10, step=1)

    subjects = {}
    for i in range(num_subjects):
        st.write(f"Subject {i+1}")
        subject_name = st.text_input(f"Subject Name {i+1}:")
        credits = st.number_input(f"Credits for {subject_name}:", min_value=1, max_value=5, step=1)
        difficulty = st.slider(f"Difficulty Level for {subject_name}:", min_value=1, max_value=5, step=1)
        subjects[subject_name] = (credits, difficulty)

    if st.button("Calculate"):
        required_grades, new_cgpa = calculate_required_grades(target_cgpa, current_cgpa, subjects)
        st.write("Predicted grades for each subject to achieve the target CGPA:")
        for subject, required_grade in required_grades.items():
            st.write(f"{subject}: {required_grade}")
        
        
        if new_cgpa > target_cgpa:
            st.write("You have underestimated yourself!")
            st.write(f"Calculated CGPA for your level: {new_cgpa:.2f}")
        else:
            st.write(f"Calculated CGPA with allotted grades: {new_cgpa:.2f}")

    st.sidebar.title("Similar Applications")
    st.sidebar.markdown("[CGPA Calculator](https://cgpacalculator-2d.streamlit.app/)")
    st.sidebar.markdown("[Grades Predictor](https://gradepredictor.streamlit.app/)")

    st.write("<p style='text-align: center;'>Crafted with fervor by 2D🤓</p>", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
