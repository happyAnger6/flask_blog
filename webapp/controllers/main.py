from flask import Blueprint, redirect, url_for, render_template, current_app
from flask.helpers import flash
from flask_login import login_user, logout_user
from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed
)

from webapp.forms import LoginForm, RegisterForm
from webapp.models import db, User

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)

@main_blueprint.route('/')
def home():
    return redirect(url_for('blog.name'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username = form.username.data
        ).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )

        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.home'))

    return render_template('login.html', form=form)

@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )
    flash("You have benn logged out.", category="success")
    return redirect(url_for('.home'))

@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Your user has been created, please login.",
              category="success")
        return redirect(url_for('.login'))

    return render_template('register.html', form=form)