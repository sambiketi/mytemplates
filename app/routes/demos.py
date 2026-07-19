


from flask import Blueprint, render_template, abort
from app.models.video import Video
from datetime import datetime

bp = Blueprint('demos', __name__, url_prefix='/demos')

@bp.route('/')
def demos():
    videos = Video.query.filter_by(is_active=True).order_by(Video.created_at.desc()).all()
    return render_template('demos.html', videos=videos, datetime=datetime)

@bp.route('/<slug>')
def demo_detail(slug):
    video = Video.query.filter_by(slug=slug, is_active=True).first()
    if not video:
        abort(404)
    return render_template('demo_detail.html', video=video, datetime=datetime)




