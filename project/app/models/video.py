


from app import db
from datetime import datetime
import re

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=True)
    video_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), default='Demo')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_embed_url(self):
        if 'youtube.com' in self.video_url or 'youtu.be' in self.video_url:
            video_id = None
            if 'youtu.be' in self.video_url:
                video_id = self.video_url.split('/')[-1].split('?')[0]
            elif 'watch?v=' in self.video_url:
                video_id = self.video_url.split('watch?v=')[1].split('&')[0]
            elif '/embed/' in self.video_url:
                video_id = self.video_url.split('/embed/')[1].split('?')[0]
            if video_id:
                return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url




