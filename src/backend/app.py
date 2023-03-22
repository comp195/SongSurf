import os
import logging
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

import artist as artist
import album 
import track

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')

with app.app_context():
    db = SQLAlchemy(app)
print("* Running on http://127.0.0.1:5000")
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

# Define route for main page (search_page)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # If user clicks SURF
        aas_searches = [] # create an empty list for storing the user's AAS searches
        
        # Get the values from each input field and add them to the list
        aas_searches.append(request.form['user_choice1']) # aas = album_artist_song_search
        aas_searches.append(request.form['user_choice2'])
        aas_searches.append(request.form['user_choice3'])
        
        # Create a new User object with the AAS searches and add it to the database
        new_user = User(aas_searches=str(aas_searches))
        try:
            db.session.add(new_user)
            db.session.commit()
            app.logger.info('Successfully added user with AAS searches: %s', aas_searches)
        except Exception as e:
            app.logger.error('Issue adding user with AAS searches %s. Error: %s', aas_searches, str(e))
            print(e)

          # If artists were chosen, treat user input as all artists, etc.
        if request.form['show_type'] == 'Artists':	# if the Artists radio button was selected
            print("Artists")
            artists = artist.get_artist(request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            user_choice = request.form['show_type']
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice, 
                recommendation1 = artists[0], 
                recommendation2 = artists[1], 
                recommendation3 = artists[2], 
                recommendation4 = artists[3], 
                recommendation5 = artists[4])
        elif request.form['show_type'] == 'Albums': # if the Albums radio button was selected
            print("Albums")
            albums = album.get_album(request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            user_choice = request.form['show_type']
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,
                recommendation1 = albums[0], 
                recommendation2 = albums[1], 
                recommendation3 = albums[2], 
                recommendation4 = albums[3], 
                recommendation5 = albums[4])
        elif request.form['show_type'] == 'Songs': # if the Songs radio button was selected
            print("Songs")
            tracks = track.get_track(request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            user_choice = request.form['show_type']
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,
                recommendation1 = tracks[0], 
                recommendation2 = tracks[1], 
                recommendation3 = tracks[2], 
                recommendation4 = tracks[3], 
                recommendation5 = tracks[4])

    else: # If user visits the page
        return render_template('home_page.html')
    
@app.route('/other_page')
def search_page():
    return render_template('search_page.html')


if __name__ == "__main__":
    app.run(debug=True)
