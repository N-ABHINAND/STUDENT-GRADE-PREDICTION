# 📊 Student Grade Prediction & Analytics Web App

A Flask-based web application designed to automate student grade calculation, performance analytics, and student record searching from uploaded Excel (`.xlsx`) or CSV (`.csv`) class datasets.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Render-blue?style=for-the-badge&logo=render)](https://student-grade-prediction-1pdh.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

---

## 🌟 Key Features

- 📁 **Multi-Format Upload Support**: Accepts `.xlsx`, `.xls`, and `.csv` files.
- 🧮 **Automated Grade Calculation**: Computes final composite score based on:
  - 📝 **Average Marks** (50% weightage)
  - 📑 **Assignment Submissions** (30% weightage)
  - 📅 **Attendance Percentage** (20% weightage)
- 📈 **Interactive Analytics Dashboard**:
  - Pass vs. Fail percentage metrics.
  - Distribution breakdown of passed/failed subjects.
  - Top 5 student leaderboard based on final numeric scores.
- 🔍 **Student Record Search**: Quickly search individual student profiles by Name, Roll Number, or Student ID.
- 🚀 **Cloud Ready**: Configured for instant deployment on [Render](https://render.com).

---

## 📐 Grading Criteria & Formula

The final numeric score for each student is computed as follows:

$$\text{Final Score} = \left(0.5 \times \frac{\text{Average Marks}}{100}\right) + \left(0.3 \times \frac{\text{Assignments Submitted}}{6}\right) + \left(0.2 \times \frac{\text{Attendance Percentage}}{100}\right)$$

### Grade Mapping Scale
| Final Score Range | Calculated Grade |
| :--- | :--- |
| $\ge 85\%$ | **A** |
| $70\% - 84.9\%$ | **B** |
| $55\% - 69.9\%$ | **C** |
| $40\% - 54.9\%$ | **D** |
| $< 40\%$ | **F** |

---

## 📁 Required Dataset Columns

To successfully process data, your uploaded `.csv` or `.xlsx` file should contain the following column headers:

- `student_name` (e.g. John Doe)
- `roll_no` (e.g. 1001)
- `id` (e.g. 9001)
- `assignments_submitted` (Number of assignments out of 6)
- `attendance_percentage` (Percentage value from 0 to 100)
- `marks_subject1`, `marks_subject2`, ... (Subject marks out of 100)

---

## 🛠️ Local Development & Running

### Prerequisites
Make sure you have Python 3 installed.

### 1. Clone the Repository
```bash
git clone https://github.com/N-ABHINAND/STUDENT-GRADE-PREDICTION.git
cd STUDENT-GRADE-PREDICTION
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask App
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## ☁️ Deployment on Render

This project is pre-configured for deployment on Render using `gunicorn`:

- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Pandas, OpenPyXL
- **Frontend**: HTML5, CSS3 (Responsive Design)
- **WSGI Server**: Gunicorn

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
