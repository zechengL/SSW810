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

class Student:
    pt_lables = ['CWID', 'Name', 'Completed Courses']
    def __init__(self, cwid, name, major):
        self._cwid = cwid
        self._name = name
        self._major = major

        self._courses = dict() #key : courses value: str with grade
        self.lables = ['CWID', 'Name', 'Major', 'Courses']

    def add_course(self, course, grade):
        self._courses[course] = grade
    
    def pt_row(self):
        return [self._cwid, self._name, self._major, sorted(self._courses.keys())]
    
    def __str__(self):
        return f'Student: {self._cwid} name: {self._name} major: {self._major} courses: {sorted(self._courses.keys())}'



class Instructor:
    pt_labels = ['CWID', 'Name', 'Department', 'Course', 'Students']
    def __init__(self, cwid, name, dept):
        self._cwid = cwid
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int) #key : courses value: no. of students in the course

    def add_student(self, course):
        self._courses[course] += 1

    def pt_row(self):
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]

    def __str__(self):
        return f'Student: {self._cwid} name: {self._name} dept: {self._dept} courses: {sorted(self._courses.keys())}'


class Repository:
    def __init__(self, wdir):
        self.wdir = wdir 
        self.students = dict()
        self.instructors = dict()
                
        self.get_students(os.path.join(wdir, 'students.txt'))
        self.get_instructors(os.path.join(wdir, 'instructors.txt'))
        self.get_grades(os.path.join(wdir, 'grades.txt'))

        print('\nStudent Summary')
        self.student_table()
        print('\nInstructor Summary')
        self.instructor_table()

    def get_students(self, path):
        try:
            for cwid, name, major in read_file(path, 3, separator = '\t', header = False):
                if cwid in self.students:
                    print (f' Warning: cwid {cwid} already read from the file')
                else:
                    self.students[cwid] = Student(cwid, name, major)
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

    def student_table(self):
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Major', 'Completed Courses'])
        for student in self.students.values():
            pt.add_row(student.pt_row())

        print(pt)
    
    def instructor_table(self):
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for instructor in self.instructors.values():
            for row in instructor.pt_row():
                pt.add_row(row)

        print(pt)

class Homework09test(unittest.TestCase):  # Test cases
    def test_student(self):
        result = Repository('C:/Users/71711/Desktop/HW09').student_table()[0]
        expect = ['10103', 'Baldwin, C', ['SSW 567', 'SSW 564', 'SSW 687', 'CS 501']]
        self.assertEqual(result, expect)
    def test_instructor(self):
        result = Repository('C:/Users/71711/Desktop/HW09').instructor_table()[0]
        expect = ['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4]
        self.assertEqual(result, expect)

def main():
    # stevens = Repository('C:/Users/71711/Desktop/HW09')
    unittest.main(exit=False, verbosity=2)

if __name__ == '__main__':
    main()

