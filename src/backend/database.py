from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError # used to roll_back duplicate items

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
    name = db.Column(db.String(120), nullable=False, unique=True)
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

    __table_args__ = ( # Prevent duplicate albums being added, by ensuring albums with the same name have a different artist
        db.UniqueConstraint('name', 'artist_id', name='uq_album_name_artist'),
    )

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

    __table_args__ = ( # Prevent duplicate tracks being added, by ensuring tracks with the same name have a different artist
        db.UniqueConstraint('name', 'artist_id', name='uq_track_name_artist'),
    )

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

class Recommend(db.Model):
    recommend_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    entity_type = db.Column(db.Enum('artist', 'album', 'track'), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    recommended = db.Column(db.Boolean, nullable=False)

    user = db.relationship('User', backref=db.backref('recommended', lazy=True)) # FK relationship

    __table_args__ = ( # Prevent duplicates by ensuring only a unique pair of entity_type and entity_id exists only once
        db.UniqueConstraint('entity_type', 'entity_id', name='uq_recommend_entity'),
        db.CheckConstraint("entity_type IN ('artist', 'album', 'track')"),
    )

""" ================== Begin Database Interface ================== """

# ----------- Album, Artist, Track information functions -----------
def get_name(item_id, item_type):
    if (item_type == 'album'):
        name = db.session.query(Album.name)\
                .filter(Album.album_id == item_id)\
                .one()
    if (item_type == 'artist'):
        name = db.session.query(Artist.name)\
                .filter(Artist.artist_id == item_id)\
                .one()
    if (item_type == 'track'):
        name = db.session.query(Track.name)\
                .filter(Track.track_id == item_id)\
                .one()
    return name
def get_image(item_id, item_type):
    if (item_type == 'album'):
        image = db.session.query(Album.image)\
                .filter(Album.album_id == item_id)\
                .one()
    if (item_type == 'artist'):
        image = db.session.query(Artist.image)\
                .filter(Artist.artist_id == item_id)\
                .one()
    if (item_type == 'track'):
        image = db.session.query(Track.image)\
                .filter(Track.track_id == item_id)\
                .one()
    return image
def get_description(item_id, item_type):
    if (item_type == 'album'):
        desc = db.session.query(Album.description)\
                .filter(Album.album_id == item_id)\
                .one()
    if (item_type == 'artist'):
        desc = db.session.query(Artist.description)\
                .filter(Artist.artist_id == item_id)\
                .one()
    if (item_type == 'track'):
        desc = db.session.query(Track.description)\
                .filter(Track.track_id == item_id)\
                .one()
    return desc
def get_release_date(item_id, item_type):
    if (item_type == 'album'):
        release_date = db.session.query(Album.release_date)\
                .filter(Album.album_id == item_id)\
                .one()
    if (item_type == 'track'):
        release_date = db.session.query(Track.release_date)\
                .filter(Track.track_id == item_id)\
                .one()
    return release_date
def get_item_object_from_id(item_id, item_type):
    if (item_type == 'album'):
        item = db.session.query(Album)\
                .filter(Album.album_id == item_id)\
                .one()
    if (item_type == 'artist'):
        item = db.session.query(Artist)\
                .filter(Artist.artist_id == item_id)\
                .one()
    if (item_type == 'track'):
        item = db.session.query(Track)\
                .filter(Track.track_id == item_id)\
                .one()
    return item
def get_album_object(album_name, album_artist):
    #ilike() means case insensitve
    album = db.session.query(Album)\
            .filter(Album.name.ilike(album_name), Album.artist.ilike(album_artist))\
            .all()
    return album
def get_artist_object(app, artist_name):
    with app.app_context():
        artist = db.session.query(Artist)\
                    .filter(Artist.name.ilike(artist_name))\
                    .first()
        return artist

def get_track_object(app, track_name, track_artist):
    with app.app_context():
        # query the artist first
        artist = get_artist_object(app, track_artist)
        if artist:
            #ilike() means case insensitve
            track = db.session.query(Track)\
                    .filter(Track.name.ilike(track_name), Track.artist_id.ilike(artist.artist_id))\
                    .all()
            return track
        else:
            print(f"No artist found with the name '{track_artist}'")
            return None

def get_tracks_from_album(album_id):
    tracks = db.session.query(Track.track_id)\
            .filter(Track.album_id == album_id)\
            .all()
    return tracks

# For optional items, use "None" if not applicable to item. Ex: artist may not have album_id, so put "none" for album_id arg
def add_item(app, item_type, item_name, item_image, item_description, item_artist_id=None, item_album_id=None, item_release_date=None):
    with app.app_context():
        if (item_type == 'album'):
            item = Album(artist_id=item_artist_id, name=item_name, image=item_image, description=item_description, release_date=item_release_date)
        elif (item_type == 'artist'):
            item = Artist(name=item_name, image=item_image, description=item_description)
        elif (item_type == 'track'):
            item = Track(album_id=item_album_id, artist_id=item_artist_id, name=item_name, image=item_image, description=item_description, release_date=item_release_date)
        
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()



# ----------- like/dislike functions -----------

def get_album_likes(user_id):
    likes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'album', LikeDislike.liked == True, LikeDislike.user_id == user_id)\
            .all()
    return likes
def get_artist_likes(user_id):
    likes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'artist', LikeDislike.liked == True, LikeDislike.user_id == user_id)\
            .all()
    return likes
def get_track_likes(user_id):
    likes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'track', LikeDislike.liked == True, LikeDislike.user_id == user_id)\
            .all()
    return likes

def get_album_dislikes(user_id):
    dislikes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'album', LikeDislike.liked == False, LikeDislike.user_id == user_id)\
            .all()
    return dislikes
def get_artist_dislikes(user_id):
    dislikes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'artist', LikeDislike.liked == False, LikeDislike.user_id == user_id)\
            .all()
    return dislikes
def get_track_dislikes(user_id):
    dislikes = db.session.query(LikeDislike.entity_id)\
            .filter(LikeDislike.entity_type == 'track', LikeDislike.liked == False, LikeDislike.user_id == user_id)\
            .all()
    return dislikes

def set_liked(user_id, item_id, item_type):
    liked = LikeDislike(user_id=user_id,entity_type=item_type,entity_id=item_id,liked=True)
    db.session.add(liked)
    db.session.commit()
def set_disliked(user_id, item_id, item_type):
    dislike = LikeDislike(user_id=user_id,entity_type=item_type,entity_id=item_id,liked=False)
    db.session.add(dislike)
    db.session.commit()

# ----------- recommendation functions -----------

def get_album_recommendations(user_id):
    recommendations = db.session.query(Recommend.entity_id)\
            .filter(Recommend.entity_type == 'album', Recommend.recommended == False, Recommend.user_id == user_id)\
            .all()
    return recommendations
def get_artist_recommendations(user_id):
    recommendations = db.session.query(Recommend.entity_id)\
            .filter(Recommend.entity_type == 'artist', Recommend.recommended == False, Recommend.user_id == user_id)\
            .all()
    return recommendations
def get_track_recommendations(user_id):
    recommendations = db.session.query(Recommend.entity_id)\
            .filter(Recommend.entity_type == 'track', Recommend.recommended == False, Recommend.user_id == user_id)\
            .all()
    return recommendations
def set_recommended(user_id, item_id, item_type):
    item = db.session.query(Recommend)\
        .filter(Recommend.user_id==user_id, Recommend.entity_id==item_id, Recommend.entity_type==item_type)\
        .one()
    item.recommended = True
    db.session.commit()



