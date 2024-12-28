from datetime import datetime
from database import db

class BucketListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))  # For grouping related items
    priority = db.Column(db.Integer, default=1)  # For ordering items

    def __repr__(self):
        return f'<BucketListItem {self.title}>'