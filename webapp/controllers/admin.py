import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint, redirect, url_for, abort, g
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from webapp.models import db, Post, Tag, Comment, User
from webapp.forms import CommentForm, PostForm
from webapp.extensions import poster_permission, admin_permission

admin_blueprint = Blueprint(
    'admin',
    __name__,
    template_folder='../templates/admin',
    url_prefix="/admin"
)

@admin_blueprint.route('/')
def home():
    tags = Tag.objects.all()
    return render_template('admin_base.html',tags = tags)

def add_all_children_tags(tag, level, all_tags):
    all_tags.append((tag.title, level))
    children_tags = Tag.objects(father=tag.title).all()
    for child_tag in children_tags:
        add_all_children_tags(child_tag, level+1, all_tags)

def get_all_tags():
    all_tags = []
    tags = Tag.objects(father=None).all()
    for tag in tags:
        add_all_children_tags(tag, 0, all_tags)
    return all_tags

@admin_blueprint.route('/tags')
def tags():
    return render_template('admin_tags.html', tags = get_all_tags)