from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    email = EmailField('Email', render_kw={"class": "form-control"}, validators=[DataRequired()])
    password = PasswordField('Mot de passe', render_kw={"class": "form-control"}, validators=[DataRequired()])
    remember_me = BooleanField("Se rappeler de moi", render_kw={"class": "form-control"})
