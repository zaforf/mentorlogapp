import bcrypt, hashlib
from flask import render_template, request, redirect, session
from app.models import db, mentorlog, slots
from app import app

@app.route('/')
@app.route('/index')
def index():
    log = reversed(mentorlog.query.order_by(mentorlog._id.desc()).limit(15).all())
    t = session.get("remove_failed", False)
    session["remove_failed"] = False
    return render_template('index.html', log=log, wrongpwd=t)

@app.route('/signup', methods = ['POST'])
def signup():
    id,mentor = request.form['id'].split()
    name = request.form['mentor-name']
    password = request.form['password']

    entry = mentorlog.query.filter_by(_id=id).first_or_404()
    setattr(entry,mentor,name)

    if password:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(),salt)
        db.session.add(slots(int(id),int(mentor[-1]),hashed[:50],salt))
    db.session.commit()
    return redirect("/")

@app.route('/remove', methods = ['POST'])
def remove():
    id, mentor = request.form['id'].split()
    password = request.form['password']

    found = slots.query.filter_by(mentorlog_id=id, mentor_number=int(mentor[-1])).first()
    if (found is None or bcrypt.hashpw(password.encode(),found.salt)[:50]==found.hash):
        print('password matches!')
        entry = mentorlog.query.filter_by(_id=id).first_or_404()
        setattr(entry,mentor,"")
        if found: db.session.delete(found)
        db.session.commit()
    else:
        print('incorrect password!')
        session["remove_failed"] = True
    
    return redirect("/")
    