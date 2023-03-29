import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

test_app = Flask(__name__)

# Specify the full path of the database file
DB_FILEPATH = os.path.join(os.path.dirname(__file__), 'instance', 'test.db')

test_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILEPATH}'

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

with test_app.app_context():
    db = SQLAlchemy(test_app)

print("* Running on http://127.0.0.1:8000")



""" Begin Database Block """
from datetime import datetime

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
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120))
    description = db.Column(db.String(1000))
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    artist = db.relationship('Artist', backref=db.backref('tracks', lazy=True)) # FK relationship
    album = db.relationship('Album', backref=db.backref('tracks', lazy=True)) # FK relationship

""" End Database Block """

with test_app.app_context():
    # reset database
    db.drop_all()
    db.create_all()



""" Begin Database Test Block """
def test_artist_album_track_classes():
    with test_app.app_context():
        # create users
        user1 = User(email='user1@example.com', password='password1')
        user2 = User(email='user2@example.com', password='password2')

        # create artists
        adele = Artist(name='Adele', image='adele.jpg', description='English singer-songwriter')
        ed_sheeran = Artist(name='Ed Sheeran', image='ed_sheeran.jpg', description='English singer-songwriter')

        # create albums
        adele_19 = Album(artist=adele, name='19', image='19.jpg', description='Debut studio album by Adele', release_date=datetime(2008, 1, 28))
        adele_21 = Album(artist=adele, name='21', image='21.jpg', description='Second studio album by Adele', release_date=datetime(2011, 1, 24))
        ed_divide = Album(artist=ed_sheeran, name='÷', image='ed_divide.jpg', description='Third studio album by Ed Sheeran', release_date=datetime(2017, 3, 3))

        # create tracks
        track1 = Track(artist=adele, album=adele_19, name='Daydreamer', image='daydreamer.jpg', description='Debut single by Adele', release_date=datetime(2007, 2, 26))
        track2 = Track(artist=adele, album=adele_19, name='Hometown Glory', image='hometown_glory.jpg', description='Second single by Adele', release_date=datetime(2007, 10, 22))
        track3 = Track(artist=adele, album=adele_21, name='Rolling in the Deep', image='rolling_in_the_deep.jpg', description='Lead single by Adele', release_date=datetime(2010, 11, 29))
        track4 = Track(artist=adele, album=adele_21, name='Someone Like You', image='someone_like_you.jpg', description='Second single by Adele', release_date=datetime(2011, 1, 24))
        track5 = Track(artist=ed_sheeran, album=ed_divide, name='Shape of You', image='shape_of_you.jpg', description='Lead single by Ed Sheeran', release_date=datetime(2017, 6, 5))
        track6 = Track(artist=ed_sheeran, album=ed_divide, name='Castle on the Hill', image='castle_on_the_hill.jpg', description='Second single by Ed Sheeran', release_date=datetime(2017, 1, 6))

        # add objects to session and commit changes
        db.session.add_all([user1, user2, adele, ed_sheeran, adele_19, adele_21, ed_divide, track1, track2, track3, track4, track5, track6])
        db.session.commit()

        # query the database
        tracks = db.session.query(Track.name)\
                        .join(Album, Track.album_id == Album.album_id)\
                        .join(Artist, Album.artist_id == Artist.artist_id)\
                        .filter(Artist.name == 'Adele', Album.name == '21')\
                        .all()

        # print the results
        for track in tracks:
            print(track.name)


#temporary
test_artist_album_track_classes()

""" End Database Test Block """