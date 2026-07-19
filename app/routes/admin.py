


from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
from app.models.product import Product
from app.models.post import Post
from app.models.video import Video
from app.models.privacy import PrivacyPolicy
from app.models.settings import SiteSettings
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import re

bp = Blueprint('admin', __name__, url_prefix='/admin')

def create_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    products_count = Product.query.count()
    posts_count = Post.query.count()
    videos_count = Video.query.count()
    return render_template('admin_dashboard.html',
                         products_count=products_count,
                         posts_count=posts_count,
                         videos_count=videos_count)

@bp.route('/products', methods=['GET', 'POST'])
@login_required
def manage_products():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')
        image_url = request.form.get('image_url')
        action_link = request.form.get('action_link')
        slug = create_slug(title)
        if Product.query.filter_by(slug=slug).first():
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
        product = Product(
            title=title,
            slug=slug,
            description=description,
            price=price,
            category=category,
            image_url=image_url or None,
            action_link=action_link or None
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('admin.manage_products'))
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin_products.html', products=products)

@bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.title = request.form.get('title')
        product.description = request.form.get('description')
        product.price = request.form.get('price')
        product.category = request.form.get('category')
        product.image_url = request.form.get('image_url') or None
        product.action_link = request.form.get('action_link') or None
        product.is_active = 'is_active' in request.form
        product.is_featured = 'is_featured' in request.form
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('admin.manage_products'))
    return render_template('admin_products_edit.html', product=product)

@bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted', 'success')
    return redirect(url_for('admin.manage_products'))

@bp.route('/blog', methods=['GET', 'POST'])
@login_required
def manage_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        content_format = request.form.get('content_format', 'html')
        slug = create_slug(title)
        if Post.query.filter_by(slug=slug).first():
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
        post = Post(
            title=title,
            slug=slug,
            content=content,
            image_url=image_url or None,
            content_format=content_format
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog post added', 'success')
        return redirect(url_for('admin.manage_blog'))
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('admin_blog.html', posts=posts)

@bp.route('/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.image_url = request.form.get('image_url') or None
        post.content_format = request.form.get('content_format', 'html')
        post.is_published = 'is_published' in request.form
        db.session.commit()
        flash('Blog post updated successfully', 'success')
        return redirect(url_for('admin.manage_blog'))
    return render_template('admin_blog_edit.html', post=post)

@bp.route('/blog/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_blog(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted', 'success')
    return redirect(url_for('admin.manage_blog'))

@bp.route('/videos', methods=['GET', 'POST'])
@login_required
def manage_videos():
    if request.method == 'POST':
        title = request.form.get('title')
        video_url = request.form.get('video_url')
        description = request.form.get('description')
        category = request.form.get('category', 'Demo')
        slug = create_slug(title)
        if Video.query.filter_by(slug=slug).first():
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"
        video = Video(
            title=title,
            slug=slug,
            video_url=video_url,
            description=description,
            category=category
        )
        db.session.add(video)
        db.session.commit()
        flash('Video added', 'success')
        return redirect(url_for('admin.manage_videos'))
    videos = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('admin_videos.html', videos=videos)

@bp.route('/videos/edit/<int:video_id>', methods=['GET', 'POST'])
@login_required
def edit_video(video_id):
    video = Video.query.get_or_404(video_id)
    if request.method == 'POST':
        video.title = request.form.get('title')
        video.video_url = request.form.get('video_url')
        video.description = request.form.get('description')
        video.category = request.form.get('category', 'Demo')
        video.is_active = 'is_active' in request.form
        db.session.commit()
        flash('Video updated successfully', 'success')
        return redirect(url_for('admin.manage_videos'))
    return render_template('admin_videos_edit.html', video=video)

@bp.route('/videos/delete/<int:video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    flash('Video deleted', 'success')
    return redirect(url_for('admin.manage_videos'))

@bp.route('/privacy', methods=['GET', 'POST'])
@login_required
def manage_privacy():
    privacy = PrivacyPolicy.query.first()
    if not privacy:
        privacy = PrivacyPolicy(content='Default privacy content.', content_format='html')
        db.session.add(privacy)
        db.session.commit()
    if request.method == 'POST':
        privacy.content = request.form.get('content')
        privacy.content_format = request.form.get('content_format', 'html')
        db.session.commit()
        flash('Privacy policy updated', 'success')
        return redirect(url_for('admin.manage_privacy'))
    return render_template('admin_privacy.html', privacy=privacy)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def manage_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    if request.method == 'POST':
        settings.logo_url = request.form.get('logo_url') or None
        settings.favicon_url = request.form.get('favicon_url') or None
        settings.site_name = request.form.get('site_name', 'myTemplates')
        settings.site_tagline = request.form.get('site_tagline', 'Premium Digital Templates')
        settings.contact_email = request.form.get('contact_email') or None
        settings.contact_phone = request.form.get('contact_phone') or None
        settings.footer_text = request.form.get('footer_text') or None
        db.session.commit()
        flash('Site settings updated', 'success')
        return redirect(url_for('admin.manage_settings'))
    return render_template('admin_settings.html', settings=settings)




