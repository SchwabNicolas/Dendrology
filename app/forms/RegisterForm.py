from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class RegisterForm(FlaskForm):
    name = StringField('Nom', render_kw={"class": "form-control"}, validators=[DataRequired()])
    email = EmailField('Email', render_kw={"class": "form-control"}, validators=[DataRequired()])
    password = PasswordField('Mot de passe', render_kw={"class": "form-control"}, validators=[DataRequired()])
