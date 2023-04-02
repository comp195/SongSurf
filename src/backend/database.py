from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    return db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Artist(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120))
    description = db.Column(db.String(1000))

class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120))
    description = db.Column(db.String(1000))
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    artist = db.relationship('Artist', backref=db.backref('albums', lazy=True)) # FK relationship

class Track(db.Model):
    track_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120))
    description = db.Column(db.String(1000))
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    artist = db.relationship('Artist', backref=db.backref('tracks', lazy=True)) # FK relationship
    album = db.relationship('Album', backref=db.backref('tracks', lazy=True)) # FK relationship

class LikeDislike(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    entity_type = db.Column(db.Enum('artist', 'album', 'track'), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    liked = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', backref=db.backref('likes_dislikes', lazy=True)) # FK relationship

    __table_args__ = (
        db.CheckConstraint("entity_type IN ('artist', 'album', 'track')"),
    )

class Reccomend(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    entity_type = db.Column(db.Enum('artist', 'album', 'track'), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    reccomended = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', backref=db.backref('reccomended', lazy=True)) # FK relationship

    __table_args__ = (
        db.CheckConstraint("entity_type IN ('artist', 'album', 'track')"),
    )

# get functions
def get_album_favorites(user):
    likes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'track', LikeDislike.liked == True)\
            .all()
    
    # add functions

    # set functions