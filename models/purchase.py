from extinsion import db
class Purchase(db.Model):
    __tablename__="purchase"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False )
    recorded_course_id = db.Column(db.Integer, db.ForeignKey("recorded.id"), nullable=False )
    payment_image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default="pending")
