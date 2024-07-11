import streamlit as st

def calculate_gpa(grades, credit_hours, previous_cgpa):
    grade_points = {
        "O": 10.0, "A+": 9.0, "A": 8.0, "B+": 7.0, "B": 6.0, "C": 5.0, "AB":0.0, "WD":0.0, "WH":0.0, "RA":0.0
    }

    total_grade_points = sum(grade_points[grade] * credit for grade, credit in zip(grades, credit_hours))
    total_credits = sum(credit_hours)

    tgpa = total_grade_points / total_credits

    gpa=(tgpa+previous_cgpa)/2
    return gpa

def main():
    st.title("GPA Calculator")

    st.header("Course Information")
    num_courses = st.number_input("Number of Courses:", min_value=1, step=1)
    previous_cgpa=st.number_input("Previous CGPA:")
    grades = []
    credit_hours = []

    for i in range(num_courses):
        st.subheader(f"Course {i+1}")
        grade = st.selectbox(f"Select Grade for Course {i+1}:", ("O", "A+", "A", "B+", "B", "C", "AB", "WD", "WH", "RA"), key=f"grade_{i}")
        credit_hour = st.selectbox(f"Select Credit Hours for Course {i+1}:", (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0), key=f"credit_{i}")
        grades.append(grade)
        credit_hours.append(credit_hour)

    if st.button("Calculate GPA"):
        gpa = calculate_gpa(grades, credit_hours, previous_cgpa)
        st.write(f"Your GPA is: {gpa:.2f}")
    
    st.sidebar.title("Similar Applications")
    st.sidebar.markdown("[CGPA Calculator](https://cgpacalculator-2d.streamlit.app/)")
    st.sidebar.markdown("[Grades Predictor](https://gradepredictor.streamlit.app/)")

    st.write("<p style='text-align: center;'>Crafted with fervor by 2D🤓</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()