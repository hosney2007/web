from extinsion import db
class Branch(db.Model):
    __tablename__ = "branches"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True ,unique=True)
    schedule = db.relationship("Schedule", backref="branch", lazy=True, cascade="all,delete")
