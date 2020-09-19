import os

# Import Canvas
from canvasapi import Canvas

# Canvas API
API_URL = "https://canvas.instructure.com/"
API_KEY = os.environ['canvas_api_key']

# Initialize Canvas object
canvas = Canvas(API_URL, API_KEY)

announcements = canvas.get_announcements()
cal_events = canvas.get_calendar_events()

courses = canvas.get_courses()
course = canvas.get_course(2353385)

user_by_id = course.get_user(8735856)
users = course.get_users(search_term='Gaurav Mehta')
tas = course.get_users(search_term='ta')

assignments = course.get_assignments()
assn = course.get_assignment(17781989)
ungraded_assn = course.get_assignments(bucket='ungraded')

subs = assn.get_submissions()
submission = assn.get_submission(user_by_id.id)

quizzes = course.get_quizzes()
quiz = course.get_quiz(0)       # insert ID
quiz.broadcast_message({
  "body": "Please take the quiz.",   # arg 0
  "recipients": "unsubmitted",       # arg 1
  "subject": "ATTENTION"             # arg 2
})

reports = quiz.get_all_quiz_reports()
questions = quiz.get_questions()
    # can also get by ID

quiz_subs = quiz.get_submissions()
quiz_sub = quiz.get_submission(0)    # insert submission ID
stats = quiz.get_statistics()