from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class mentorlog(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    section = db.Column(db.String(10))
    mentor1 = db.Column(db.String(50))
    mentor2 = db.Column(db.String(50))
    mentor3 = db.Column(db.String(50))
    mentor4 = db.Column(db.String(50))
    def __init__(self, date, section, mentor1, mentor2, mentor3, mentor4):
        self.date = date
        self.section = section 
        self.mentor1 = mentor1
        self.mentor2 = mentor2
        self.mentor3 = mentor3
        self.mentor4 = mentor4

class slots(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    mentorlog_id = db.Column(db.Integer, db.ForeignKey('mentorlog.id'))
    mentor_number = db.Column(db.Integer)
    hash = db.Column(db.String(50))
    salt = db.Column(db.String(50))

    mentorlog = db.relationship('mentorlog', backref=db.backref('slots', lazy=True))

    def __init__(self, mentorlog_id, mentor_number, hash, salt):
        self.mentorlog_id = mentorlog_id
        self.mentor_number = mentor_number
        self.hash = hash
        self.salt = salt