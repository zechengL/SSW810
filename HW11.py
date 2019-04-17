#Homework09
#Zecheng

import os
import unittest
from prettytable import PrettyTable
from collections import defaultdict

def read_file(path, number, separator='\t', header=False):
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError('%s is not a file' % (path))
    else:
        with fp:
            count = 0
            try:
                for line in fp:
                    count += 1
                    if header:  
                        header = False
                        continue
                    words = line.strip().split(separator) 
                    if len(words) != number:
                        raise ValueError('%s has %s fields on line %s but expected %s' % (path, len(words), count, number))
                    yield tuple(words)
            except ValueError as err:
                print('ValueError', err)

class Major:
    pt_labels = ['Major', 'Required Courses', 'Electives']
    def __init__(self, dept):
        self.dept = dept
        self.required = set()
        self.electives = set()

    def add_majors(self, flag, course):
        if flag.upper() == 'E':
            self.electives.add(course)
        elif flag.upper() == 'R':
            self.required.add(course)
        else:
            raise ValueError(f'Flag {flag} is invalid for course {course}')

    def summary(self):
        return [self.dept, sorted(self.required), sorted(self.electives)]


class Student:
    pt_lables = ['CWID', 'Name', 'Completed Courses']
    def __init__(self, cwid, name, major, couse_list):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses_list = couse_list
        self.courses = dict()

    def add_course(self, course, grade):
        self.courses[course] = grade
    
    def summary(self):
        c_course = list()
        for k,v in self.courses.items():
            if v in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
                c_course.append(k)
        r_required = self.courses_list.required - set(c_course)
        if set(c_course) & self.courses_list.electives:
            r_electives = 'none'
        else:
            r_electives = sorted(self.courses_list.electives)
        return([self.cwid, self.name, self.major, sorted(c_course), sorted(r_required), r_electives])


class Instructor:
    pt_labels = ['CWID', 'Name', 'Department', 'Course', 'Students']
    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int) #key : courses value: no. of students in the course

    def add_student(self, course):
        self.courses[course] += 1

 def summary(self):
        DB_FILE = 'D:/git/810/810_startup.db'
        db = sqlite3.connect(DB_FILE)
        # for (k,v) in self.courses.items():
        #     yield [self.cwid, self.name, self.dept, k, v]
        for row in db.execute('SELECT CWID, Name, Dept, Course, COUNT(*) as cnt FROM Instructors JOIN Grades ON Instructors.CWID = Grades.Instructor_CWID GROUP BY Course'):
            yield row


class Repository:
    def __init__(self, wdir):
        self.wdir = wdir 
        self.students = dict()
        self.instructors = dict()
        self.majors = dict()

        self.get_majors(os.path.join(wdir, 'majors.txt'))        
        self.get_students(os.path.join(wdir, 'students.txt'))
        self.get_instructors(os.path.join(wdir, 'instructors.txt'))
        self.get_grades(os.path.join(wdir, 'grades.txt'))

        print('\nStudent Summary')
        self.student_table()
        print('\nInstructor Summary')
        self.instructor_table()

    def get_majors(self, path):
        try:
            for major, flag, course in read_file(path, 3, separator='\t', header=False):
                if major not in self.majors:
                    self.majors[major] = Major(major)
                self.majors[major].add_majors(flag, course)
        except ValueError as e:
            print(e)        

    def get_students(self, path):
        try:
            for cwid, name, major in read_file(path, 3, separator = '\t', header = False):
                if cwid in self.students:
                    print (f' Warning: cwid {cwid} already read from the file')
                else:
                    self.students[cwid] = Student(cwid, name, major, self.majors[major])
        except ValueError as e:
            print(e)

    def get_instructors(self, path):
        try:
            for cwid, name, dept in read_file(path, 3, separator = '\t', header = False):
                if cwid in self.instructors:
                    print (f' Warning: cwid {cwid} already read from the file')
                else:
                    self.instructors[cwid] = Instructor(cwid, name, dept)
        except ValueError as e:
            print(e)

    def get_grades(self, path):
        try:
            for student_cwid, course, grade, instructor_cwid in read_file(path, 4, separator = '\t', header = False):
                if student_cwid in self.students:
                    self.students[student_cwid].add_course(course, grade) #tell student abt new course and grade
                else:
                    print (f' Warning: student cwid {student_cwid} is not known in the file') 
            
                if instructor_cwid in self.instructors:
                    self.instructors[instructor_cwid].add_student(course) #tell student abt new course and grade
                else:
                    print (f' Warning: instructor cwid {instructor_cwid} is not known in the file') 
        except ValueError as e:
            print (e) 

    def major_table(self):
        return_result = list()  # save the list for test
        pt = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        for major in self.majors.values():
            pt.add_row(major.summary())
            return_result.append(major.summary())
        print(pt)
        return return_result

    def student_table(self):
        return_result = list()  # save the list for test
        pt = PrettyTable(field_names=['CWID', 'Name', 'Major','Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for student in self.students.values():
            pt.add_row(student.summary())
            return_result.append(student.summary())
        print(pt)
        return return_result
    
    def instructor_table(self):
        return_result = list()  # save the list for test
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for instructor in self.instructors.values():
            for x in instructor.summary():
                pt.add_row(x)
                return_result.append(x)
        print(pt)
        return return_result

class Homework09test(unittest.TestCase):  # Test cases
    def test_student(self):
        result = Repository('C:/Users/71711/Desktop/HW09').student_table()[0]
        expect = ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], 'none']
        self.assertEqual(result, expect)
    def test_instructor(self):
        result = Repository('C:/Users/71711/Desktop/HW09').instructor_table()[0]
        expect = ['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4]
        self.assertEqual(result, expect)
    def test_major(self):
        result = Repository('C:/Users/71711/Desktop/HW09').major_table()[0]
        expect = ['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']]
        self.assertEqual(result, expect)

def main():
    
    wdir = r'C:/Users/71711/Desktop/HW09'
    unittest.main(exit=False, verbosity=2)

if __name__ == '__main__':
    main()

