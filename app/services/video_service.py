


from app import db
from app.models.video import Video
from datetime import datetime

class VideoService:
    @staticmethod
    def get_all():
        return Video.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_latest(limit=3):
        return Video.query.filter_by(is_active=True).order_by(Video.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_by_slug(slug):
        return Video.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    @staticmethod
    def get_by_category(category):
        return Video.query.filter_by(category=category, is_active=True).all()
    
    @staticmethod
    def create(data):
        video = Video(
            title=data['title'],
            video_url=data['video_url'],
            description=data.get('description'),
            category=data.get('category', 'Demo')
        )
        db.session.add(video)
        db.session.commit()
        return video
    
    @staticmethod
    def update(video, data):
        video.title = data.get('title', video.title)
        video.video_url = data.get('video_url', video.video_url)
        video.description = data.get('description', video.description)
        video.category = data.get('category', video.category)
        video.is_active = data.get('is_active', video.is_active)
        db.session.commit()
        return video
    
    @staticmethod
    def delete(video):
        db.session.delete(video)
        db.session.commit()




