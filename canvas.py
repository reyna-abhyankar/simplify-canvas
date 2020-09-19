import os

# Import Canvas
from canvasapi import Canvas

# Canvas API
API_URL = "https://canvas.instructure.com/"
API_KEY = "7~a0WZUQK2LiJBRU9GBGIIb99it5rA8MMB8Jt5ANEv0C2ilgi0hgwsztOVPebnT0DD"

# Initialize Canvas object
canvas = Canvas(API_URL, API_KEY)

courses = canvas.get_courses()
course = canvas.get_course(2353385)

user_by_id = course.get_user(8735856)
users = course.get_users(search_term='Gaurav Mehta')
tas = course.get_users(search_term='ta')


assn = course.get_assignment(17781989)
ungraded_assn = course.get_assignments(bucket='ungraded')

subs = assn.get_submissions()
submission = assn.get_submission(user_by_id.id)

quizzes = course.get_quizzes()
quiz = course.get_quiz(6126370)       # insert ID
# quiz.broadcast_message({
#   "body": "Please take the quiz.",   # arg 0
#   "recipients": "unsubmitted",       # arg 1
#   "subject": "ATTENTION"             # arg 2
# })

reports = quiz.get_all_quiz_reports()
questions = quiz.get_questions()
    # can also get by ID

quiz_subs = quiz.get_submissions()
#quiz_sub = quiz.get_submission(6126370)    # insert submission ID
stats = quiz.get_statistics()

studentSize = 0
users = course.get_users(enrollment_type=['student'])
for user in users:
  studentSize=studentSize+1

teacherSize = 0
users = course.get_users(enrollment_type=['teacher'])
for user in users:
  teacherSize=teacherSize+1

taSize = 0
users = course.get_users(enrollment_type=['ta'])
for user in users:
  taSize=taSize+1

print("Teachers: "+str(teacherSize))
print("TAs: "+str(taSize))
print("Students: "+str(studentSize))


assignments = course.get_assignments()

for assignment in assignments:
  print(assignment)
#/quizlist
#/assignmentlist
#/help