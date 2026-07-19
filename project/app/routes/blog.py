


from flask import Blueprint, render_template, abort
from app.models.post import Post
from datetime import datetime

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
def blog():
    posts = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).all()
    return render_template('blog.html', posts=posts, datetime=datetime)

@bp.route('/<slug>')
def blog_detail(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first()
    if not post:
        abort(404)
    return render_template('blog_detail.html', post=post, datetime=datetime)




