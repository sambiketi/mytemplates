


from app import db
from app.models.post import Post
from datetime import datetime

class BlogService:
    @staticmethod
    def get_all():
        return Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).all()
    
    @staticmethod
    def get_latest(limit=3):
        return Post.query.filter_by(is_published=True).order_by(Post.date_posted.desc()).limit(limit).all()
    
    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    @staticmethod
    def create(data):
        post = Post(
            title=data['title'],
            content=data['content'],
            image_url=data.get('image_url'),
            content_format=data.get('content_format', 'html')
        )
        db.session.add(post)
        db.session.commit()
        return post
    
    @staticmethod
    def update(post, data):
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        post.image_url = data.get('image_url', post.image_url)
        post.content_format = data.get('content_format', post.content_format)
        post.is_published = data.get('is_published', post.is_published)
        db.session.commit()
        return post
    
    @staticmethod
    def delete(post):
        db.session.delete(post)
        db.session.commit()




