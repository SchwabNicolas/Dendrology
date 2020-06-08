from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from mongoengine import *
import json


@login.user_loader
def load_user(id):
    user = User.objects(id=id)[0]
    return user


class User(UserMixin, Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    is_admin = BooleanField(required=True, unique=True)
    password_hash = StringField(required=True)

    # Méthode permettant de retourner la classe au format Json
    def json(self):
        return json.dumps(self.dictionary())

    # Setter le hash du mot de passe
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checker le hash du mot de passe
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Méthode retournant un dictionnaire contenant les variables de la classe
    def dictionary(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash
        }

    # Métadonnées de la classe
    # indexes => valeurs que l'on veut indexer dans la requête (sont généralement uniques)
    # ordering => valeurs par lesquelles on voudra trier la requête
    meta = {
        "indexes": ["email"],
        "ordering": ["name"]
    }
