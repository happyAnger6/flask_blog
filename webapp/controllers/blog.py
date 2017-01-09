import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint, redirect, url_for

from webapp.models import db, Post, Tag, Comment, User, tags
from webapp.forms import CommentForm, PostForm

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder=path.join(path.pardir,'templates','blog'),
    url_prefix="/blog"
)

def sidebar_data():
    recent = Post.query.order_by(
        Post.publish_date.desc()
    ).limit(5).all()

    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags

def with_sidebar_render(template,**kwargs):
    recent, top_tags = sidebar_data()
    kwargs.setdefault('recent',recent)
    kwargs.setdefault('top_tags',top_tags)

    return render_template(template,**kwargs)

@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.publish_date.desc()
    ).paginate(page,10)

    return with_sidebar_render(
        'home.html',
        posts = posts
    )


@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()

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
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()

        db.session.add(new_post)
        db.session.commit()

    return render_template('new.html', form=form)

@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.publish_date = datetime.datetime.now()

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', post_id=post.id))

    form.text.data = post.text
    return render_template('edit.html', form=form, post=post)
