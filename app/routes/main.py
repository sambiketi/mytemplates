


from flask import Blueprint, render_template, session, request, jsonify
from app.models.product import Product
from app.models.post import Post
from app.models.video import Video
from app.models.gallery import Gallery
from app.models.user import User
from app.models.privacy import PrivacyPolicy
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    featured_products = Product.query.filter_by(is_active=True, is_featured=True).limit(4).all()
    all_products = Product.query.filter_by(is_active=True).all()
    latest_posts = Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).limit(3).all()
    latest_videos = Video.query.filter_by(is_active=True).order_by(Video.created_at.desc()).limit(3).all()
    gallery_items = Gallery.query.order_by(Gallery.created_at.desc()).limit(20).all()
    admin = User.query.first()
    
    return render_template('index.html',
                         featured_products=featured_products,
                         all_products=all_products,
                         latest_posts=latest_posts,
                         latest_videos=latest_videos,
                         gallery=gallery_items,
                         admin=admin,
                         datetime=datetime)

@bp.route('/robots.txt')
def robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Sitemap: /sitemap.xml"
    ]
    return "\n".join(lines), 200, {'Content-Type': 'text/plain'}

@bp.route('/sitemap.xml')
def sitemap():
    products = Product.query.filter_by(is_active=True).all()
    posts = Post.query.filter_by(is_published=True).all()
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    
    static_pages = ['/', '/products', '/blog', '/demos', '/gallery', '/privacy']
    for page in static_pages:
        xml.append(f'  <url><loc>https://mytemplates.com{page}</loc><priority>0.8</priority></url>')
    
    for product in products:
        xml.append(f'  <url><loc>https://mytemplates.com/products/{product.slug}</loc><priority>0.9</priority></url>')
    
    for post in posts:
        xml.append(f'  <url><loc>https://mytemplates.com/blog/{post.slug}</loc><priority>0.7</priority></url>')
    
    xml.append('</urlset>')
    return "\n".join(xml), 200, {'Content-Type': 'application/xml'}

@bp.route('/ping')
def ping():
    return "OK", 200

@bp.route('/health')
def health_check():
    try:
        from app import db
        from sqlalchemy import text
        db.session.execute(text("SELECT 1"))
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500




