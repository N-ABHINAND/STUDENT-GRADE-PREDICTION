from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def calculate_grades(df):
    marks_cols = [col for col in df.columns if col.startswith('marks_')]
    max_assignments = 6

    df['avg_marks'] = df[marks_cols].mean(axis=1)
    df['assignment_score'] = df['assignments_submitted'] / max_assignments
    df['attendance_score'] = df['attendance_percentage'] / 100
    df['final_numeric_score'] = (0.5 * df['avg_marks'] / 100) + (0.3 * df['assignment_score']) + (0.2 * df['attendance_score'])

    def score_to_grade(score):
        if score >= 0.85:
            return 'A'
        elif score >= 0.7:
            return 'B'
        elif score >= 0.55:
            return 'C'
        elif score >= 0.4:
            return 'D'
        else:
            return 'F'
    df['calculated_grade'] = df['final_numeric_score'].apply(score_to_grade)
    return df

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return "No file uploaded"
    
    df = pd.read_excel(file)
    df = calculate_grades(df)

    passing_mark = 40
    marks_cols = [col for col in df.columns if col.startswith('marks_')]
    df['subjects_passed'] = df[marks_cols].ge(passing_mark).sum(axis=1)

    total_students = len(df)
    top_5 = df.nlargest(5, 'final_numeric_score')[['student_name', 'id', 'calculated_grade']].to_dict('records')

    passed_all = (df['subjects_passed'] == len(marks_cols)).sum()
    passed_4 = (df['subjects_passed'] == 4).sum()
    passed_3 = (df['subjects_passed'] == 3).sum()
    passed_2 = (df['subjects_passed'] == 2).sum()
    passed_1 = (df['subjects_passed'] == 1).sum()

    failed_5 = (df['subjects_passed'] == 0).sum()
    failed_4 = (df['subjects_passed'] == 1).sum()
    failed_3 = (df['subjects_passed'] == 2).sum()
    failed_2 = (df['subjects_passed'] == 3).sum()
    failed_1 = (df['subjects_passed'] == 4).sum()

    # Use smart criteria: passing if passed 3 or more subjects
    students_passed = (df['subjects_passed'] >= 3).sum()
    students_failed = total_students - students_passed

    pass_percent = round((students_passed / total_students) * 100, 1)
    fail_percent = round((students_failed / total_students) * 100, 1)

    summary_stats = {
        'total_students': total_students,
        'passed_all': passed_all,
        'passed_4': passed_4,
        'passed_3': passed_3,
        'passed_2': passed_2,
        'passed_1': passed_1,
        'failed_5': failed_5,
        'failed_4': failed_4,
        'failed_3': failed_3,
        'failed_2': failed_2,
        'failed_1': failed_1,
        'pass_percent': pass_percent,
        'fail_percent': fail_percent
    }

    df.to_csv('last_data.csv', index=False)
    return render_template(
        'dashboard.html',
        tables=[df.to_html(classes='data')],
        titles=df.columns.values,
        stats=summary_stats,
        top_5=top_5
    )

@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()
    try:
        df = pd.read_csv('last_data.csv')
    except Exception:
        return redirect(url_for('home'))

    result = df[(df['student_name'].str.lower().str.contains(query)) |
                (df['roll_no'].astype(str).str.contains(query)) |
                (df['id'].astype(str).str.contains(query))]

    if not result.empty:
        student = result.iloc[0].to_dict()  # First matched student
        subject_marks = [(col.replace('_', ' ').title(), student[col]) for col in df.columns if col.startswith('marks_')]
        return render_template('student_search.html', student=student, subject_marks=subject_marks, query=query)
    else:
        return render_template('student_search.html', student=None, subject_marks=[], query=query)

if __name__ == '__main__':
    app.run(debug=True)
