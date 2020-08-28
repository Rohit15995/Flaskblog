from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',\
         validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username.')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('E-mail ID is already in use. Please use another e-mail ID.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',\
         validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')
    image_file = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])
    
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different username.')
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('E-mail ID is already in use. Please use another e-mail ID.')
