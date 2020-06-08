from mongoengine import *
import json


# Définition de la classe servant de modèle
class Tree(Document):

    # Nom scientifique de l'arbre
    scientific_name = StringField(required=True, max_length=100)
    # Auteurs du nom scientifique de l'arbre
    authors = StringField(required=True, max_length=200)
    # Famille de l'arbre
    family = StringField(required=True, max_length=100)
    # Nom vulgaire de l'arbre
    common_name = StringField(required=True, max_length=100)
    # Page descriptive sur le site InfoFlora
    infoflora_page = StringField(max_length=200)
    # Page descriptive sur le site Wikipedia
    wikipedia_page = StringField(max_length=200)
    # Nom de fichier de l'image de l'arbre
    img_filename = StringField()
    # Conifère, feuillus, palmier ou bambou
    tree_type = StringField(required=True)
    # Néophyte invasive
    invasive_neophyte = BooleanField()
    # Comestibilité
    edibility = StringField(required=True)

    # Méthode permettant de retourner la classe au format Json
    def json(self):
        return json.dumps(self.dictionary())

    # Méthode retournant un dictionnaire contenant les variables de la classe
    def dictionary(self):
        return {
            "scientific_name": self.scientific_name,
            "authors": self.authors,
            "family": self.family,
            "common_name": self.common_name,
            "infoflora_page": self.infoflora_page,
            "wikipedia_page": self.wikipedia_page,
            "img_filename": self.img_filename,
            "tree_type": self.tree_type,
            "invasive_neophyte": self.invasive_neophyte,
            "edibility": self.edibility
        }

    # Métadonnées de la classe
    # indexes => valeurs que l'on veut indexer dans la requête (sont généralement uniques)
    # ordering => valeurs par lesquelles on voudra trier la requête
    meta = {
        "indexes": ["scientific_name", "common_name", "family"],
        "ordering": ["scientific_name", "common_name", "family"]
    }
