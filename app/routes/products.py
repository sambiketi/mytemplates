


from flask import Blueprint, render_template, abort
from app.models.product import Product
from datetime import datetime

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/')
def products():
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).all()
    return render_template('products.html', products=products, datetime=datetime)

@bp.route('/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if not product:
        abort(404)
    return render_template('product_detail.html', product=product, datetime=datetime)




