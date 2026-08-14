#imports======================///
from flask import Blueprint, render_template,redirect,request,url_for,flash,current_app
from models.recorded import Recorded
from flask_login import login_required,current_user
from extinsion import db
from models.lesson import Lessons
from models.purchase import Purchase
from werkzeug.utils import secure_filename
import os
from utils.decorators import admin_required,save_image

recorded = Blueprint("recorded",__name__)

#============[RECORDED PAGE]====////
@recorded.route("/courses/recorded", methods=["POST", "GET"])
def recorded_page():
    recorded = Recorded.query.all()
    purchases ={}
    if current_user.is_authenticated:
        user_purchases = Purchase.query.filter_by(user_id=current_user.id).all()
        purchases ={purchase.recorded_course_id: purchase
                   for purchase in user_purchases
                   }
    return render_template("recorded.html", recorded=recorded ,purchases=purchases)

#=======RECORDED COURSES=====//
@recorded.route("/admin/recorded", methods=["POST", "GET"])
@login_required
@admin_required
def recorded_courses(): 
    recorded = Recorded.query.all()
    return render_template("admin/recorded.html" ,recorded=recorded , name= "recorded")

#========ADD COURSE====///
@recorded.route("/admin/recorded/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_course():

    if request.method == "POST":
        thumbnail = request.files["thumbnail"]
        filename = secure_filename(thumbnail.filename)
        thumbnail.save(os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            ))

        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        new_recorded = Recorded(
            title = title,
            description= description,
            price=price,
            thumbnail=filename
        )  
        db.session.add(new_recorded)
        db.session.commit()
        flash("recorded course added successfuly ")
        return redirect(url_for("recorded.recorded_courses"))
    return render_template("admin/add-recorded.html" , name="add Course") 

#=======EDIT=====//
@recorded.route("/admin/recorded/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_course( id ):

    recorded = Recorded.query.get_or_404(id)
    if request.method == "POST":

        recorded.title = request.form.get("title")
        recorded.description = request.form.get("description")
        recorded.price = request.form.get("price")
        db.session.commit()
        flash("recorded course updated successfully")
        return redirect(url_for("recorded.recorded_courses"))
    return render_template("admin/edit-recorded.html", recorded=recorded, name="Edit Course") 

#====DELETE=====////
@recorded.route("/admin/recorded/delete/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_course( id ):

    recorded = Recorded.query.get_or_404(id)
    if recorded.purchase:
        flash("you can't delete this course because it has orders","danger")
        return redirect(url_for("recorded.recorded_courses"))    
    db.session.delete(recorded)
    db.session.commit()
    return redirect(url_for("recorded.recorded_courses"))
#===============================LESSONS=====================================================///

#==========LESSON VIEW====///
@recorded.route("/admin/recorded/<int:id>/lesson", methods=["POST", "GET"])
@login_required
@admin_required
def lessons(id):  
    recorded = Recorded.query.get_or_404(id)
    lessons = Lessons.query.filter_by(
        recorded_course_id=id
    ).order_by(Lessons.lesson_order).all()
    return render_template("admin/lessons.html" ,recorded=recorded ,lesson=lessons ,name= "recorded")
#======ADD LESSON====///

@recorded.route("/admin/recorded/<int:id>/lesson/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_lesson(id):
    recorded = Recorded.query.get_or_404(id)
    if request.method == "POST":
        lesson=Lessons(
          title = request.form["title"],
        video_links = request.form["video_links"],
        lesson_order = request.form["lesson_order"],
        recorded_course_id=recorded.id
   
        )
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for("recorded.lessons", id=recorded.id))
    return render_template("admin/add-lesson.html", recorded=recorded ,name="add lesson")   

#=======EDIT LESSON=======///
@recorded.route("/admin/lesson/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_lesson( id ):

    lesson = Lessons.query.get_or_404(id)
    if request.method == "POST":
        lesson.title = request.form["title"]
        lesson.video_links = request.form["video_links"]
        lesson.lesson_order = request.form["lesson_order"]

        db.session.commit()
        flash("recorded course updated successfully")
        return redirect(url_for("recorded.lessons", id=lesson.recorded_course_id))
    return render_template("admin/edit-lesson.html", lesson=lesson, name="Edit lesson") 

#==============DELETE LESSON======///
@recorded.route("/admin/lesson/delete/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def delete_lesson( id ):

    lesson = Lessons.query.get_or_404(id)

    db.session.delete(lesson)
    db.session.commit()
    return redirect(url_for("recorded.lessons",id = lesson.recorded_course_id ))
#==========================================PAYMENTS=======================================================////

#=======BUY=====///

#=================ORDERS======================////
@recorded.route("/admin/orders", methods=["GET", "POST"])
@login_required
@admin_required
def orders():
    orders = Purchase.query.order_by(Purchase.id.desc()).all()
    return render_template("admin/orders.html", orders=orders)

#====== APPROVE ORDERS======///
@recorded.route("/admin/orders/<int:id>/approve")
@login_required
@admin_required
def approve_order(id):
    order = Purchase.query.get_or_404(id)
    order.status = "approved"
    db.session.commit()
    return redirect(url_for("recorded.orders"))

#==========REJECT ORDERS====///
@recorded.route("/admin/orders/<int:id>/reject")
@login_required
@admin_required
def reject_order(id):
    order = Purchase.query.get_or_404(id)
    order.status = "rejected"
    db.session.commit()
    return redirect(url_for("recorded.orders"))

#==============DELETE order======///
@recorded.route("/admin/orders/<int:id>/delete", methods=["GET", "POST"])
@login_required
@admin_required
def delete_order( id ):

    order = Purchase.query.get_or_404(id)

    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("recorded.orders"))

#==========PAYMENTS PAGE=====///
@recorded.route("/courses/recorded/<int:id>/payment", methods=["GET", "POST"])
@login_required
def payment(id):
    # الكورس
    recorded = Recorded.query.get_or_404(id)

    # عملية الشراء الخاصة بالمستخدم
    purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        recorded_course_id=id
    ).first()
    
    # رفع الصورة
    if request.method == "POST":

        image = request.files.get("payment_image")

        if image and image.filename != "":
            if purchase is None:
              purchase = Purchase(
              user_id=current_user.id,
              recorded_course_id=id,
              status="pending"
            )
   
            db.session.add(purchase)


            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            purchase.payment_image = filename
            purchase.status = "waiting"

            db.session.commit()

            flash("Payment uploaded successfully.", "success")

            return redirect(url_for("recorded.recorded_page"))

        flash("Please choose an image.", "danger")

    return render_template(
        "payment.html",
        recorded=recorded,
        purchase=purchase,
        name=recorded.title
    )

#==========STUDENT LESSON PAGE=======///

@recorded.route("/recorded/<int:course_id>/lessons")
@login_required
def course_lessons(course_id):

    recorded = Recorded.query.get_or_404(course_id)

    purchase = Purchase.query.filter_by(
        user_id=current_user.id,
        recorded_course_id=course_id
    ).first_or_404()

    if not purchase:
        flash("You must purchase this course first.", "danger")
        return redirect(url_for("recorded.payment", id=course_id))

    if purchase.status != "approved":
        flash("Your payment is still under review.", "warning")
        return redirect(url_for("recorded.recorded_page"))

    lessons = Lessons.query.filter_by(
        recorded_course_id=course_id
    ).order_by(Lessons.lesson_order).all()

    if not lessons:
        flash("No lessons available.", "warning")
        return redirect(url_for("recorded.recorded_page"))

    lesson_id = request.args.get("lesson", type=int)

    if lesson_id:
        lesson = Lessons.query.filter_by(
            id=lesson_id,
            recorded_course_id=course_id
        ).first_or_404()

        if lesson is None:
            lesson = lessons[0]
    else:
        lesson = lessons[0]

    return render_template(
        "lessons.html",
        recorded=recorded,
        lesson=lesson,
        lessons=lessons,
        name=recorded.title
    )
