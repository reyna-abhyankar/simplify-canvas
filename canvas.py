import os

# Import Canvas
from canvasapi import Canvas

# Canvas API
API_URL = "https://canvas.instructure.com/"
API_KEY = "7~a0WZUQK2LiJBRU9GBGIIb99it5rA8MMB8Jt5ANEv0C2ilgi0hgwsztOVPebnT0DD"

# Initialize Canvas object
def main():
  canvas = Canvas(API_URL, API_KEY)
  courses = canvas.get_courses()
  course = canvas.get_course(course_id) #hardcode or sys argv to get course_id

if __name__ == "__main__":
    main()

def user_info(user_id,course):
  user_by_id = course.get_user(user_id)
  users = course.get_users(search_term='Gaurav Mehta')
  tas = course.get_users(search_term='ta')

def assignment_info(assign_id,course):
  assn = course.get_assignment(assign_id)
  ungraded_assn = course.get_assignments(bucket='ungraded')

def submission_check(user_by_id,assn):
  subs = assn.get_submissions()
  submission = assn.get_submission(user_by_id.id)

def quiz_message(quiz_id,course):        #uncomment out message stuff?
  quizzes = course.get_quizzes()
  quiz = course.get_quiz(quiz_id)       # insert ID
# quiz.broadcast_message({
#   "body": "Please take the quiz.",   # arg 0
#   "recipients": "unsubmitted",       # arg 1
#   "subject": "ATTENTION"             # arg 2
# })

def quiz_report(quiz):
  reports = quiz.get_all_quiz_reports()
  questions = quiz.get_questions()
    # can also get by ID

def get_quiz_submissions(quiz,quiz_id):
  quiz_subs = quiz.get_submissions()
  #quiz_sub = quiz.get_submission(6126370)    # insert submission ID
  stats = quiz.get_statistics()

def get_students(course):
  studentSize = 0
  users = course.get_users(enrollment_type=['student'])
  for user in users:
    studentSize+=1

def get_teachers(course):
  teacherSize = 0
  users = course.get_users(enrollment_type=['teacher'])
  for user in users:
    teacherSize+=1

def get_tA(course):

  taSize = 0
  users = course.get_users(enrollment_type=['ta'])
  for user in users:
    taSize+=1

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