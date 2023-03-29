from app import db

# Create User model with columns for the attributes
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True) # User_ID Column
    aas_searches = db.Column(db.String(300), nullable=False) # "album_artist_song_search" Column
    song_favorites = db.Column(db.String(300), nullable=False) # Song Favorites Column
    artist_favorites = db.Column(db.String(300), nullable=False) # Artist Favorites Column
    album_favorites = db.Column(db.String(300), nullable=False) # Album Favorites Column

    def __init__(self, aas_searches="", song_favorites="", artist_favorites="", album_favorites=""):
        self.aas_searches = aas_searches
        self.song_favorites = song_favorites
        self.artist_favorites = artist_favorites
        self.album_favorites = album_favorites

    def __repr__(self):
        return '<User_id %r>' % self.user_id