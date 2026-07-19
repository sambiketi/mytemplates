


from flask import Blueprint, render_template
from app.models.gallery import Gallery
from datetime import datetime

bp = Blueprint('gallery', __name__, url_prefix='/gallery')

@bp.route('/')
def gallery():
    gallery_items = Gallery.query.order_by(Gallery.created_at.desc()).all()
    return render_template('gallery.html', gallery=gallery_items, datetime=datetime)




