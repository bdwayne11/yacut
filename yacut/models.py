from datetime import datetime
from urllib.parse import urljoin

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(512), nullable=False, unique=True)
    short = db.Column(db.String(6), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=urljoin('http://localhost/', self.short),
        )
