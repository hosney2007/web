#imports============///
from flask import Blueprint, render_template
from models.course import Course

course = Blueprint("course", __name__)

@course.route("/admin/course", methods=["POST", "GET"])
def courses():
    course = Course.query.all()
    return render_template("admin/course.html" ,course=course, name= "Courses")

@course.route("/courses/offline")
def offline_courses():
    courses = Course.query.filter_by(course_type="offline").all()
    return render_template("offline.html", course=courses)

@course.route("/courses/online")
def online_courses():
    courses = Course.query.filter_by(course_type="online").all()
    return render_template("online.html", course=courses)

