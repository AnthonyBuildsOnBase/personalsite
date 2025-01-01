from datetime import datetime
from database import db

class BucketListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.Integer, default=1)  # For ordering items
    target_year = db.Column(db.Integer, nullable=True)  # Year to complete the item, nullable for backlog
    tags = db.Column(db.String(200))  # Comma-separated tags

    def __repr__(self):
        return f'<BucketListItem {self.title}>'

    @property
    def tag_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in (self.tags or '').split(',') if tag.strip()]