from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from ..models import Users


# 建立登入表單
class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired()])
    email = StringField("Mail", validators=[DataRequired()])
    favorite_song = StringField("Favorite Song")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField('Password', validators=[DataRequired(),EqualTo('password_hash2', message='Need To Comfirm Password')])
    password_hash2 = PasswordField('Confirm', validators=[DataRequired()])
    profile_pic = FileField("Picture")
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')
    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one')  
class PasswordForm(FlaskForm):
    email = StringField("Main", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ForgotPasswordFrom(FlaskForm):
    email = StringField("Enter your user account's verified email address and we will send you a password reset link.", validators=[DataRequired()])
    submit = SubmitField("Send password reset email")
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
class SetForgotPasswordFrom(FlaskForm):
    password_hash = PasswordField('Password', validators=[DataRequired(),EqualTo('password_hash2', message='Need To Comfirm Password')])
    password_hash2 = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField("Reset password")