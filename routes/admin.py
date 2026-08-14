#imoprts=============================///
from flask import Blueprint, render_template, request, redirect, url_for,current_app,flash
from flask_login import  current_user, login_required
from extinsion import db
from models.course import Course
from models.branch import Branch
from models.schedaule import Schedule
from models.success_story import SuccessStory
from werkzeug.utils import secure_filename
import os
from utils.decorators import admin_required
import uuid

admin = Blueprint("admin" ,__name__)
# ===================admindashboard==========////
@admin.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    courses = Course.query.filter_by( is_active=True).all()
    return render_template("admin/admin-dashboard.html" ,user=current_user, course=courses, name="Admin")

#==============addd courses==================////

@admin.route("/admin/add-course", methods=["GET", "POST"])
@login_required
@admin_required
def add_course():
    if request.method == "POST":
        image = request.files["image"]
        filename = secure_filename(image.filename)
        image.save(os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            ))
        
        title = request.form["title"]
        description = request.form["description"]
        course_type = request.form["course_type"]    
        course = Course(
            title = title,
            description= description,
            course_type=course_type,
            image=filename
        )  
        db.session.add(course)
        db.session.commit()
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("admin/add-course.html", name="add Course")      

#edit courses
@admin.route("/admin/edit-course/<int:course_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course( course_id ):
    course = Course.query.get_or_404(course_id)
    if request.method == "POST":

        course.title = request.form["title"]
        course.description = request.form["description"]
        course.course_type = request.form["course_type"]

        db.session.commit()
        flash("course edited", "success")
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("admin/edit-course.html", course=course, name="Edit Course")   


#=================delete courses=========//////
@admin.route("/admin/delete-course/<int:course_id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_course( course_id ):
    course = Course.query.get_or_404(course_id)
    if course.schedule:
        flash("you can't delete this course because it has groups","danger")
        return redirect(url_for("course.courses"))
        
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("admin.admin_dashboard"))

#==============================groups===============================================
#=========add group=========///
@admin.route("/admin/add-group", methods=["GET", "POST"])
@login_required
@admin_required
def add_group():
    courses = Course.query.all()
    branches = Branch.query.all()
    if request.method == "POST":

        course_id = request.form.get("course_id")
        level = request.form.get("level")
        mode = request.form.get("mode")
        branch_id = request.form.get("branch_id")
        day1 = request.form.get("day1")
        time1 = request.form.get("time1")
        day2 = request.form.get("day2")
        time2 = request.form.get("time2")
        if mode == "online":
            branch_id = None
        
    
        schedule = Schedule(
            course_id=course_id,
            level=level,
            mode=mode,
            branch_id=branch_id,
            day1=day1,
            time1=time1,
            day2=day2,
            time2=time2

        )  
        db.session.add(schedule)
        db.session.commit()
        return redirect(url_for("admin.admin_dashboard"))
    return render_template("admin/add-group.html", course=courses, branches=branches, name="Add Group")      


#====branch==////
@admin.route("/admin/branch", methods=["POST", "GET"])
@login_required
@admin_required
def branch():
    branch = Branch.query.all()
    return render_template("admin/branch.html" ,branch=branch, name= "Branches")

@admin.route("/admin/add-branch", methods=["GET", "POST"])
@login_required
@admin_required
def add_branch():
    if request.method == "POST":

        name = request.form.get("name")
        branch = Branch(
            name=name
        )
            
        db.session.add(branch)
        db.session.commit()
        return redirect(url_for("admin.branch"))
    return render_template("admin/add-branch.html")  

@admin.route("/admin/delete-branch/<int:branch_id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_branch( branch_id ):
    branch = Branch.query.get_or_404(branch_id)
    if branch.schedule:
        flash("you can't delete this course because it has groups","danger")
        return redirect(url_for("admin.branch"))
        
    db.session.delete(branch)
    db.session.commit()
    return redirect(url_for("admin.branch"))


#========successs story====///
@admin.route("/success-stories")
@login_required
@admin_required
def success_stories():

    stories = SuccessStory.query.order_by(
        SuccessStory.id.desc()
    ).all()

    return render_template(
        "admin/success_stories.html",
        stories=stories,
        name="Success Stories"
    )
#add===============
@admin.route("/success-stories/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_success_story():

    if request.method == "POST":

        student_name = request.form.get("student_name")
        subject = request.form.get("subject")
        before_score = request.form.get("before_score")
        after_score = request.form.get("after_score")
        review = request.form.get("review")

        image = request.files.get("image")

        if not image:
            flash("Please upload a student image.", "danger")
            return redirect(url_for("admin.add_success_story"))

        filename = secure_filename(image.filename)

        extension = filename.rsplit(".", 1)[1].lower()

        new_filename = f"{uuid.uuid4()}.{extension}"

        image.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                new_filename
            )
        )

        story = SuccessStory(

            student_name=student_name,

            subject=subject,

            before_score=before_score,

            after_score=after_score,

            review=review,

            image=new_filename

        )

        db.session.add(story)

        db.session.commit()

        flash("Success story added successfully.", "success")

        return redirect(url_for("admin.success_stories"))

    return render_template(
        "admin/add_success_story.html",
        name="Add Success Story"
    )
# edit============
@admin.route("/success-stories/edit/<int:story_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_success_story(story_id):

    story = SuccessStory.query.get_or_404(story_id)

    if request.method == "POST":

        story.student_name = request.form.get("student_name")
        story.subject = request.form.get("subject")
        story.before_score = request.form.get("before_score")
        story.after_score = request.form.get("after_score")
        story.review = request.form.get("review")

        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(image.filename)
            extension = filename.rsplit(".", 1)[1].lower()
            new_filename = f"{uuid.uuid4()}.{extension}"

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    new_filename
                )
            )

            story.image = new_filename

        db.session.commit()

        flash("Success story updated successfully.", "success")

        return redirect(url_for("admin.success_stories"))

    return render_template(
        "admin/edit_success_story.html",
        story=story,
        name="Edit Success Story"
    )
#delete====================
@admin.route("/success-stories/delete/<int:story_id>", methods=["POST"])
@login_required
@admin_required
def delete_success_story(story_id):

    story = SuccessStory.query.get_or_404(story_id)

    db.session.delete(story)

    db.session.commit()

    flash("Success story deleted successfully.", "success")

    return redirect(url_for("admin.success_stories"))
