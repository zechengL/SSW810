from flask import Flask, render_template
import sqlite3

DB_FILE = 'C:/Users/71711/Desktop/HW12/810_startup.db'

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome'

@app.route('/instructors')
def instructors_summary():
    query = 'SELECT CWID, Name, Dept, Course, COUNT(*) as cnt FROM Instructors JOIN Grades ON Instructors.CWID = Grades.Instructor_CWID GROUP BY Course'
    db = sqlite3.connect(DB_FILE)
    rows = db.execute(query)
    data = [{'cwid': cwid, 'name': name, 'department': department, 'course': course, 'stdnumber': stdnumber} for cwid, name, department, course, stdnumber in rows]
    db.close()
    return render_template('instructors_table.html',title="Instructors",table_title="Instructors Summary",instructors=data)

app.run(debug=True)