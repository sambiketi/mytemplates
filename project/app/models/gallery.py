


from app import db
from datetime import datetime

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item_id,
            'source': self.source,
            'image_url': self.image_url,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }




