from flask import render_template, url_for, flash, \
                  redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from test_flask_lesson import db
from test_flask_lesson.models import Post, Comment, Like
from test_flask_lesson.posts.forms import PostForm, CommentForm


posts = Blueprint('posts', __name__)

@posts.route('/allposts')
@login_required
def allposts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).\
            paginate(page=page, per_page=5)
    return render_template('allposts.html', posts=posts)

@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.comment_text.data,
            post_id=post_id,
            username=current_user.username
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment added!', 'success')
        return redirect(f'/post/{post_id}')
    return render_template(
        'post.html',
        title=post.title,
        post=post,
        form=form
    )

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post was created!', 'success')
        return redirect(url_for('posts.allposts'))
    return render_template(
        'create_post.html',
        title='New post',
        form=form,
        legend='New post'
    )

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post was updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        'create_post.html',
        title='Updatte post',
        form=form,
        legend='Update post'
    )

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted!', 'success')
    return redirect(url_for('posts.allposts'))

@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.username != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment was deleted', 'success')
    return redirect(f'/post/{comment.post_id}')

@posts.route("/post/<int:post_id>/like")
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        abort(403)
    like = Like(
        post_id=post_id,
        username=current_user.username
    )
    db.session.add(like)
    db.session.commit()
    flash('Your like was added!', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

