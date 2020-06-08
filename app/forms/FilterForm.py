from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class FilterForm(FlaskForm):
    scientific_name = StringField('Nom scientifique', render_kw={"placeholder": "Nom scientifique", "class": "form-control"})
    common_name = StringField('Nom vernaculaire', render_kw={"placeholder": "Nom vernaculaire", "class": "form-control"})
    family = SelectField('Famille', coerce=str, render_kw={"class": "form-control"})
