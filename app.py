import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def calculate_grades(df):
    marks_cols = [col for col in df.columns if col.startswith('marks_')]
    if not marks_cols:
        raise ValueError("No columns starting with 'marks_' (e.g. marks_subject1) found in the file.")

    if 'assignments_submitted' not in df.columns or 'attendance_percentage' not in df.columns:
        raise ValueError("File is missing required columns: 'assignments_submitted' or 'attendance_percentage'.")

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
    try:
        file = request.files.get('file')
        if not file or not file.filename:
            return render_template('upload.html', error="No file selected. Please choose a file to upload.")

        filename = file.filename.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file)
        else:
            return render_template('upload.html', error="Invalid file type. Please upload a .csv or .xlsx file.")

        df = calculate_grades(df)

        passing_mark = 40
        marks_cols = [col for col in df.columns if col.startswith('marks_')]
        df['subjects_passed'] = df[marks_cols].ge(passing_mark).sum(axis=1)

        total_students = len(df)
        if total_students == 0:
            return render_template('upload.html', error="The uploaded file contains no data rows.")

        cols_to_show = [c for c in ['student_name', 'id', 'calculated_grade'] if c in df.columns]
        top_5 = df.nlargest(5, 'final_numeric_score')[cols_to_show].to_dict('records')

        passed_all = int((df['subjects_passed'] == len(marks_cols)).sum())
        passed_4 = int((df['subjects_passed'] == 4).sum())
        passed_3 = int((df['subjects_passed'] == 3).sum())
        passed_2 = int((df['subjects_passed'] == 2).sum())
        passed_1 = int((df['subjects_passed'] == 1).sum())

        failed_5 = int((df['subjects_passed'] == 0).sum())
        failed_4 = int((df['subjects_passed'] == 1).sum())
        failed_3 = int((df['subjects_passed'] == 2).sum())
        failed_2 = int((df['subjects_passed'] == 3).sum())
        failed_1 = int((df['subjects_passed'] == 4).sum())

        students_passed = int((df['subjects_passed'] >= 3).sum())
        students_failed = total_students - students_passed

        pass_percent = round((students_passed / total_students) * 100, 1) if total_students > 0 else 0
        fail_percent = round((students_failed / total_students) * 100, 1) if total_students > 0 else 0

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
    except Exception as e:
        return render_template('upload.html', error=f"Error processing file: {str(e)}")

@app.route('/search')
def search():
    query = request.args.get('query', '').strip().lower()
    if not os.path.exists('last_data.csv'):
        return redirect(url_for('home'))
    try:
        df = pd.read_csv('last_data.csv')
    except Exception:
        return redirect(url_for('home'))

    if query and not df.empty:
        cond = pd.Series([False] * len(df))
        if 'student_name' in df.columns:
            cond |= df['student_name'].astype(str).str.lower().str.contains(query, na=False)
        if 'roll_no' in df.columns:
            cond |= df['roll_no'].astype(str).str.lower().str.contains(query, na=False)
        if 'id' in df.columns:
            cond |= df['id'].astype(str).str.lower().str.contains(query, na=False)

        result = df[cond]
        if not result.empty:
            student = result.iloc[0].to_dict()
            subject_marks = [(col.replace('_', ' ').title(), student[col]) for col in df.columns if col.startswith('marks_')]
            return render_template('student_search.html', student=student, subject_marks=subject_marks, query=query)

    return render_template('student_search.html', student=None, subject_marks=[], query=query)

if __name__ == '__main__':
    app.run(debug=True)

