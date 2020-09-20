import os
import sys

# Import Canvas
from canvasapi import Canvas


# Canvas API
API_URL = "https://canvas.instructure.com/"
API_KEY = os.environ['canvas_api_key']

# Variables
UNGRADED = 'ungraded'
COURSES = 'courses'
CHECKSUB = 'submissions'
BROADCAST = 'broadcast'
#QUIZ_REPORT = 'quizreport'
QUIZ_STAT = 'quizstat'
QUIZZES = 'quizzes'
TOTAL_NUMBER = 'count'
ASSIGNMENTS = 'assignments'
STUDENT_IDS = 'studentids'

def main(command, arg2, arg3, arg4):
  canvas = Canvas(API_URL, API_KEY)
  courses = canvas.get_courses()
  #course = canvas.get_course(course_id) #hardcode or sys argv to get course_id

  argSplit = command.lower()
  course = canvas.get_course(2353385)
  if(argSplit == UNGRADED):
    course = canvas.get_course(arg2)
    ungraded_assignments(course)
  elif(argSplit == COURSES):
    for course in courses:
      print(course)
  elif(argSplit == CHECKSUB):
    assignment = course.get_assignment(arg3)
    submission_check(arg2,assignment)
  elif(argSplit == BROADCAST):
    quiz_message(canvas.get_course(arg2),arg3,arg4)
  #elif(argSplit == QUIZ_REPORT):
  #  quiz_report(course.get_quiz(arg2))
  elif(argSplit == QUIZ_STAT):
    get_quiz_submissions(course.get_quiz(arg2))
  elif(argSplit == TOTAL_NUMBER):
    num_students(canvas.get_course(arg2))
  elif(argSplit == ASSIGNMENTS):
    print_assignments(course)
  elif(argSplit == QUIZZES):
    print_quizzes(course)
  elif(argSplit == 'studentids'):
    student_id(course)
  else:
    help(arg2)

# Deprecated
def user_info(user_id,course):
  user_by_id = course.get_user(user_id)
  users = course.get_users(search_term='Gaurav Mehta')
  tas = course.get_users(search_term='ta')

def ungraded_assignments(course):
  ungraded_assn = course.get_assignments(bucket='ungraded')
  for assignment in ungraded_assn:
    print(assignment)

###### NEED PRINT
def submission_check(user_by_id,assn):
  subs = assn.get_submissions()
  submission = assn.get_submission(user_by_id.id)
  print(submission)

###### NEED PRINT
def quiz_message(course,subject,body):
  quiz = course.get_quiz(6128124)  # currently quiz 1
  quiz.broadcast_message({"body": body, "recipients": "all", "subject": subject})
  print("Message broadcasted!", end='')

# Deprecated
def quiz_report(quiz):
  reports = quiz.get_all_quiz_reports()
  for report in reports:
    print(report['student_analysis'])

def get_quiz_submissions(quiz):
  stats = quiz.get_statistics()
  stat = stats[0]
  sub_stat = stat.submission_statistics
  print("Submissions: ", sub_stat['unique_count'])
  print("Average: %0.2f" % float(sub_stat['score_average']))
  print("High: %d" % int(sub_stat['score_high']))
  print("Low: %d" % int(sub_stat['score_low']))
  print("Standard Deviation: %0.2f" % float(sub_stat['score_stdev']))
  print("Average Time Spent: %d seconds" % int(sub_stat['duration_average']))

def num_students(course):
  studentSize = 0
  users = course.get_users(enrollment_type=['student'])
  for user in users:
    studentSize+=1

  teacherSize = 0
  users = course.get_users(enrollment_type=['teacher'])
  for user in users:
    teacherSize+=1

  taSize = 0
  users = course.get_users(enrollment_type=['ta'])
  for user in users:
    taSize+=1
  
  print("%s students" % studentSize)
  print("%s teachers" % teacherSize)
  print("%s TAs" % taSize)

def student_id(course):
  studentSize = 0
  users = course.get_users(enrollment_type=['student'])
  for user in users:
    print(user)

def print_quizzes(course):
  quizzes = course.get_quizzes()
  for quiz in quizzes:
    print(quiz)

def print_assignments(course):
  assignments = course.get_assignments()
  
  for assignment in assignments:
    if assignment.name[0]=='H':
      print(assignment)

def help(input):
  if(input == UNGRADED):
    print("Gets the list of assignments that you haven't graded yet\n")
    print("Usage: %s [course_id]" % UNGRADED)
  elif(input == COURSES):
    print("Displays all of your courses and their course ID\n")
    print("Usage: %s" % COURSES)
  elif(input == CHECKSUB):
    print("Checks if a student has submitted an assignment\n")
    print("Usage: %s [user_id] [assignment_id]" % CHECKSUB)
  elif(input == BROADCAST):
    print("Sends a message to all students' canvas inboxes and emails\n")
    print("Usage: %s [course_id] [subject] [message]" % BROADCAST)
    print("Ex: broadcast 2353385 ATTENTION Technical difficulties!!")
  #elif(input == QUIZ_REPORT):
  #  print("Gets quiz report\n")
  #  print("Usage: %s [quiz_id]" % QUIZ_REPORT)
  elif(input == QUIZ_STAT):
    print("Instantly see statistics for any given quiz\n")
    print("Usage: %s [quiz]" % QUIZ_STAT)
  elif(input == QUIZZES):
    print("Get all the quizzes for a class\n")
    print("Usage: %s" % QUIZZES)
  elif(input == TOTAL_NUMBER):
    print("Quickly obtain the number of students, TAs, and teachers for a course\n")
    print("Usage: %s [course_id]" % TOTAL_NUMBER)
  elif(input == ASSIGNMENTS):
    print("Print all homework assignments for a class\n")
    print("Usage: %s [course_id]" % ASSIGNMENTS)
  elif(input == STUDENT_IDS):
    print("Get all student IDs\n")
    print("Usage: %s [course_id]" % STUDENT_IDS)
  else:
    print("Here is a list of all commands, please use help <command> for more info on specific commands. Case doesn't matter!\n")
    print("%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s" % 
      (UNGRADED, COURSES, CHECKSUB, BROADCAST, QUIZ_STAT, QUIZZES, TOTAL_NUMBER, ASSIGNMENTS, STUDENT_IDS))

if __name__ == "__main__":
  args = sys.argv[1].split(' ')
  cmd = args[0]
  arg2 = ''
  arg3 = ''
  arg4 = ''
  s = ''
  count = len(args)
  if count > 1:
    arg2 = args[1]
  if count > 2:
    arg3 = args[2]
  if count > 3:
    arg4 = args[3]

  if count >= 4:
    del args[0:3]
    for word in args:
      s += word
      s += ' '
    arg4 = s
  main(cmd, arg2, arg3, arg4)
  sys.stdout.flush()
