from app import app
from .models.Tree import *
from .models.auth.User import *
from .config import config
from .forms.TreeForm import TreeForm
from .forms.FilterForm import FilterForm
from .forms.LoginForm import LoginForm
from .forms.RegisterForm import RegisterForm
from .utils.taxo_utils import count_genera
from .decorators.AdminPermissionsRequired import admin_perms_required
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import random


@app.route('/')
@app.route('/index/')
@app.route('/home/')
def index():
    rnd_trees = random.choices(population=Tree.objects, k=3)
    families_number = len(Tree.objects().distinct('family'))
    genera_number = count_genera(Tree.objects().distinct('scientific_name'))
    species_number = Tree.objects.count()
    return render_template('index.html',
                           rnd_trees=rnd_trees,
                           families_number=families_number,
                           genera_number=genera_number,
                           species_number=species_number)


@app.route('/trees', methods=('GET', 'POST'))
def trees():
    # Filter form
    form = FilterForm()
    families = Tree.objects().distinct('family')
    form.family.choices = [(f, f) for f in families]
    form.family.choices.insert(0, ("Toutes", "Toutes"))
    form.family.default = "Toutes"

    # Filter request
    trees_f = Tree.objects.order_by('+family', '+scientific_name')
    if request.method == 'POST':
        if request.form.get("filter_search") is not None:
            family = request.form.get("family")
            family = family if family is not None else ""
            family = family if family != form.family.default else ""
            common_name = request.form.get("common_name")
            common_name = common_name if common_name is not None else ""
            scientific_name = request.form.get("scientific_name")
            scientific_name = scientific_name if scientific_name is not None else ""
            if request.form.get("family") != form.family.default or scientific_name != "" or common_name != "":
                trees_f = Tree.objects(family__icontains=family, common_name__icontains=common_name,
                                       scientific_name__icontains=scientific_name)

    return render_template('trees.html',
                           trees=trees_f,
                           nb_trees=trees_f.count(),
                           form=form)


@app.route('/tree', methods=('GET', 'POST'))
def tree():
    id = request.args.get("id")
    tree = Tree.objects(id=id)[0]
    return render_template('tree.html',
                           tree=tree)


@login_required
@app.route('/add_tree/', methods=('GET', 'POST'))
def add_tree():
    form = TreeForm()
    if form.validate_on_submit():
        fn = secure_filename(form.image.data.filename)
        form.image.data.save(
            os.path.join(
                config.IMAGE_UPLOAD_FOLDER, fn
            )
        )
        tree = Tree(
            scientific_name=form.scientific_name.data,
            common_name=form.common_name.data,
            authors=form.authors.data,
            family=form.family.data,
            infoflora_page=form.infoflora_page.data,
            tree_type=form.tree_type.data,
            wikipedia_page=form.wikipedia_page.data,
            edibility=form.edibility.data,
            invasive_neophyte=form.invasive_neophyte.data,
            img_filename=fn
        ).save()
        return redirect('/manage/')
    return render_template('add_tree.html', form=form)


@admin_perms_required
@app.route('/manage/')
def manage():
    return render_template('manage.html',
                           trees=Tree.objects)


@login_required
@app.route('/remove_tree', methods=('GET', 'POST'))
def remove_tree():
    id = request.args.get("id")
    tree = Tree.objects(id=id)[0]
    if tree.img_filename is not None:
        os.remove(os.path.join(
            config.IMAGE_UPLOAD_FOLDER, tree.img_filename
        ))
    tree.objects(id=id).delete()
    return redirect('/manage/')


@login_required
@app.route('/edit_tree', methods=('GET', 'POST'))
def edit_tree():
    id = request.args.get("id")
    tree = Tree.objects(id=id)[0]
    form = TreeForm(data=tree.dictionary())
    if form.validate_on_submit():

        tree.scientific_name = form.scientific_name.data
        tree.common_name = form.common_name.data
        tree.infoflora_page = form.infoflora_page.data
        tree.authors = form.authors.data
        tree.family = form.family.data
        tree.edibility = form.edibility.data
        tree.invasive_neophyte = form.invasive_neophyte.data
        tree.wikipedia_page = form.wikipedia_page.data
        tree.tree_type = form.tree_type.data

        if form.image.data is not None:
            if hasattr(form.image.data, 'filename'):
                fn = secure_filename(form.image.data.filename)
                os.remove(os.path.join(
                    config.IMAGE_UPLOAD_FOLDER, tree.img_filename
                ))
                form.image.data.save(
                    os.path.join(
                        config.IMAGE_UPLOAD_FOLDER, fn
                    )
                )
                tree.img_filename = fn
        print(tree.dictionary())
        Tree.objects(id=id).update(**tree.dictionary())
        return redirect('/manage/')
    return render_template('edit_tree.html', form=form, trees=trees, id=id, tree=tree)


@app.route('/license')
def site_license():
    return render_template('license.html')


# AUTHENTIFICATION

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        user.save()
        user = User.objects(email=form.email.data)[0]
        if user is None or not user.check_password(form.password.data):
            flash('Un problème est survenu, veuillez réessayer')
            return redirect(url_for('register'))
        login_user(user, remember=False)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data)[0]
        if user is None or not user.check_password(form.password.data):
            flash('Email ou mot de passe invalide')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
