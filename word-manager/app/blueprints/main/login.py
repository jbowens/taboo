import hashlib
from app.blueprints.main import main
from app.models.admin import Admin
from flask import render_template, request, current_app, redirect, session

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        hasher = hashlib.sha256()
        hasher.update(request.form.get('password'))
        passhash = hasher.hexdigest()
        match = Admin.query.filter_by(username=request.form.get('username'),\
               passwordhash=passhash).first()
        if match:
            session['logged_in'] = True
            session['admin_aid'] = match.aid
            return redirect('/')
        else:
            render_template('login.html')
    return render_template('login.html')
