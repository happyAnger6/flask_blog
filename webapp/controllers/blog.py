import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint, redirect, url_for, abort, g
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from webapp.models import db, Post, Tag, Comment, User
from webapp.forms import CommentForm, PostForm
from webapp.extensions import poster_permission, admin_permission

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder=path.join(path.pardir,'templates','blog'),
    url_prefix="/blog"
)

def sidebar_data():
    recent = Post.objects.limit(5).all()

    top_tags = []
    return recent, top_tags

def with_sidebar_render(template,**kwargs):
    recent, top_tags = sidebar_data()
    kwargs.setdefault('recent',recent)
    kwargs.setdefault('top_tags',top_tags)

    return render_template(template,**kwargs)

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.objects.order_by("-publish_date").paginate(page,10)

    return with_sidebar_render(
        'home.html',
        posts = posts
    )


@blog_blueprint.route('/post/<string:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    post = Post.objects(id=post_id).get_or_404()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.date = datetime.datetime.now()
        post.comments.append(new_comment)
        post.save()
    tags = post.tags
    comments = post.comments

    return with_sidebar_render(
        'post.html',
        post = post,
        tags = tags,
        comments = comments,
        form = form
    )

@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()

    return with_sidebar_render(
        'tag.html',
        tag = tag,
        posts = posts
    )

@blog_blueprint.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()

    return with_sidebar_render(
        'user.html',
        user = user,
        posts = posts
    )

@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    print("new_post")
    if form.validate_on_submit():
        new_post = Post()
        new_post.title = form.title.data
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        user = User.objects(id=current_user.id).first()
        new_post.user = user
        new_post.save()

    return render_template('new.html', form=form)

@blog_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.objects(id=id).get_or_404()
    permission = Permission(UserNeed(post.user.id))

    if(permission.can() or admin_permission.can()):
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()

            post.save()

            return redirect(url_for('.post', post_id=post.id))

        form.text.data = post.text
        return render_template('edit.html', form=form, post=post)
    abort(403)