import os
import sys

# Import Canvas
from canvasapi import Canvas


# Canvas API
API_URL = "https://canvas.instructure.com/"
#API_KEY = "7~a0WZUQK2LiJBRU9GBGIIb99it5rA8MMB8Jt5ANEv0C2ilgi0hgwsztOVPebnT0DD"
API_KEY = os.environ['canvas_api_key']

# Initialize Canvas object

def main(command, arg2, arg3, arg4):
  canvas = Canvas(API_URL, API_KEY)
  courses = canvas.get_courses()
  #course = canvas.get_course(course_id) #hardcode or sys argv to get course_id

  argSplit = command.lower()
  course = canvas.get_course(2353385)
  if(argSplit == 'ungraded'):
    course =canvas.get_course(arg2)
    ungraded_assignments(course)
  elif(argSplit == 'checksub'):
    assignment = course.get_assignment(arg3)
    submission_check(arg2,assignment)
  elif(argSplit == 'broadcast'): #TODO:print list of quiz 
    quiz_message(arg2,arg3,course)
  elif(argSplit == 'quizreport'):
    quiz_report(arg2)
  elif(argSplit == 'quizsub'):
   quiz = course.get_quiz 
   get_quiz_submissions(quiz)
  elif(argSplit == 'totalnumber'):
    num_students(canvas.get_course(arg2))
  elif(argSplit == 'assignments'):
    print_assignments(course)
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
def quiz_message(first,second,course):
  #quizzes = course.get_quizzes()
  quiz = course.get_quiz(6128124)
  quiz.broadcast_message({"body": second, "recipients": "all", "subject": first})
  print("Message broadcasted!", end='')

###### NEED PRINT
def quiz_report(quiz):
  reports = quiz.get_all_quiz_reports()
  for report in reports:
    print(report)
    # can also get by ID

def get_quiz_submissions(quiz):
  quiz_subs = quiz.get_submissions()
  #quiz_sub = quiz.get_submission(6126370)    # insert submission ID
  stats = quiz.get_statistics()
  print(stats)


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
  print(studentSize+" students")
  print(taSize+" TAs")

def student_id(course):
  studentSize = 0
  users = course.get_users(enrollment_type=['student'])
  for user in users:
    print(user)

#print("Teachers: "+str(teacherSize))
#print("TAs: "+str(taSize))
#print("Students: "+str(studentSize))


def print_assignments(course):
  assignments = course.get_assignments()
  
  for assignment in assignments:
    print(assignment)
#/quizlist
#/assignmentlist
#/help

def help(input):
  if(input == "ungraded"):
    print("Prints out all the ungraded assignments\n")
    print("Ex: ungraded [course_id]")
  elif(input == "checksub"):
    print("For a given user id see if they submitted a specific assignment\n")
    print("Ex: checksub [user_id] [assignment_id]")
  elif(input == "msgquiz"):
    print("Use this cmd to broadcast a message to students during a quiz\n")
    print("Ex: msgquiz [quiz_id]")
  elif(input == "quizreport"):
    print("Gets quiz report\n")
    print("Ex: quizreport [quiz_id]")
  elif(input == "quizsub"):
    print("Prints out statistics relating to a specific quiz id\n")
    print("Ex: quizsub [quiz]")
  elif(input == "totalnumber"):
    print("Displays the total number of users enrolled in the class\n")
    print("Ex: totalnumber [course_id]")
  elif(input == "printassignments"):
    print("Prints out all assignments for the class\n")
    print("Ex: printassignments [course_id]")
  elif(input == "studentids"):
    print("Displays student name and associated user id number\n")
    print("studentids [course_id]")
  else:
    print("Here is a list of all commands, please use help+desiredcommand for more info on specific commands")
    print("ungraded\nchecksub\nmsgquiz\nquizreport\nquizsub\ntotalnumber\nprintassignments\nstudentids")




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

  if count > 4:
    del args[0:2]
    for word in args:
      s += word
      s += ' '
    arg3 = s
  main(cmd, arg2, arg3, arg4)
  sys.stdout.flush()
