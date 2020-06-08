from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class TreeForm(FlaskForm):
    scientific_name = StringField('Nom scientifique', validators=[DataRequired()])
    common_name = StringField('Nom vernaculaire', validators=[DataRequired()])
    authors = StringField('Auteurs', validators=[DataRequired()])
    family = StringField('Famille', validators=[DataRequired()])
    infoflora_page = StringField('Fiche InfoFlora')
    wikipedia_page = StringField('Fiche Wikipedia')
    edibility = SelectField('Comestibilité', coerce=str, choices=[("not", "Non comestible"), ("edi", "Comestible"), ("pha", "Pharmaceutique"), ("tox", "Toxique"), ("mor", "Mortel")])
    invasive_neophyte = BooleanField('Néophyte invasif')
    tree_type = SelectField('Type', coerce=str, choices=[("con", "Conifère"), ("bro", "Feuillu"), ("bam", "Bambou"), ("pal", "Palmier")])
    image = FileField('Image')
