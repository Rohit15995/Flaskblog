from flaskblog.models import User,Post
import os,secrets
from flaskblog import app, db, bcrypt, login_manager
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask import render_template,url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author':'Daft Punk',
        'title':'Harder, Better, Faster, Stronger',
        'content':'Work it harder, make it better, do it faster, makes us stronger',
        'date_posted':'October 2001'
    },
    {
        'author':'Foo fighters',
        'title':'Walk',
        'content':"I'm learning to walk again, I believe I've waited long enough",
        'date_posted':'June 17 2011'
    }
]

@app.route("/")
@app.route("/index")

def index():
    return render_template('index.html',posts=posts)
    
@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login.','success')
        return redirect(url_for('login'))
        
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f"Welcome { form.email.data }", 'success')
            return redirect(url_for('index'))
        else:
            flash("Incorrect username or password. Please try again.",'danger')    
    return render_template("login.html", title="Login", form=form)


def save_picture(image_file):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(image_file.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static\\profile_pictures', image_name)
    image_file.save(image_path)

    return image_name



@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_name = save_picture(form.image_file.data)
            current_user.image_file = image_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for('account'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename='profile_pictures/'+ current_user.image_file)
    return render_template("account.html", title="My Account", image_file=image_file, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))