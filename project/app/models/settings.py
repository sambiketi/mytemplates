


from app import db
from datetime import datetime

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    logo_url = db.Column(db.String(500), nullable=True)
    favicon_url = db.Column(db.String(500), nullable=True)
    site_name = db.Column(db.String(100), default='myTemplates')
    site_tagline = db.Column(db.String(200), default='Premium Digital Templates')
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    footer_text = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_site_config(self):
        return {
            'logo_url': self.logo_url,
            'favicon_url': self.favicon_url,
            'site_name': self.site_name,
            'site_tagline': self.site_tagline,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'footer_text': self.footer_text
        }




