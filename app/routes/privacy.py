


from flask import Blueprint, render_template
from app.models.privacy import PrivacyPolicy
from datetime import datetime

bp = Blueprint('privacy', __name__, url_prefix='/privacy')

@bp.route('/')
def privacy():
    privacy = PrivacyPolicy.query.first()
    if not privacy:
        privacy = PrivacyPolicy(content="Default privacy policy content.", content_format='html')
    return render_template('privacy.html', privacy=privacy, datetime=datetime)




