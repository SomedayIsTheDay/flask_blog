from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from sqlalchemy import desc

from flask_blog import db
from flask_blog.models import Post
from .forms import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/posts")
@login_required
def allposts():
    page = request.args.get("page", 1, type=int)
    ord_posts = Post.query.order_by(desc(Post.date_posted)).paginate(
        page=page, per_page=5
    )
    return render_template("posts.html", posts=ord_posts)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("posts.allposts"))
    return render_template(
        "create_post.html", title="New post", form=form, legend="New post"
    )


@posts.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.show_post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Updating post", form=form, legend="Updating post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts.allposts"))
