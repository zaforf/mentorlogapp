from flask import Flask
from datetime import datetime, date, timedelta
from app.models import db, mentorlog, slots
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = '85685fdd5ecc6a95b38d17fc'
db.init_app(app)

with app.app_context():
    db.create_all()
    today = datetime.combine(date.today(), datetime.min.time())
    nextwednesday = today+timedelta(days=(7+2-today.weekday())%7)
    nextthursday = nextwednesday+timedelta(days=1)
    for i in range(5):
        if not (mentorlog.query.filter_by(date=nextwednesday).first()):
            db.session.add(mentorlog(nextwednesday, "Science", *[""]*4))
        if not (mentorlog.query.filter_by(date=nextthursday).first()):
            db.session.add(mentorlog(nextthursday, "Math", *[""]*4))
        nextwednesday+=timedelta(days=7)
        nextthursday+=timedelta(days=7)
    db.session.commit()

from app import routes