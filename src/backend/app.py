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
print("* Running on http://127.0.0.1:8000")
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

        # Check if any input fields are empty
        if not request.form['user_choice1'] or not request.form['user_choice2'] or not request.form['user_choice3']:
        	error_message = "Please fill out all three input fields."
        	return render_template('search_page.html', message=error_message)

        # Check if a radio button is selected
        if not request.form.get('show_type'):
        	error_message = "Please select a category: Artists, Albums, or Songs"
        	return render_template('search_page.html', message=error_message)

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

        loading = "Loading..."

          # If artists were chosen, treat user input as all artists, etc.
        if request.form['show_type'] == 'Artists':	# if the Artists radio button was selected
            print("Artists")
            artists = artist.get_artist(request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            user_choice = request.form['show_type']
            recommendations = [artists[0], artists[1], artists[2], artists[3], artists[4]]
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,recommendations=recommendations)
        elif request.form['show_type'] == 'Albums': # if the Albums radio button was selected
            print("Albums")
            albums = album.get_album((request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            user_choice = request.form['show_type']
            recommendations = [albums[0], albums[1], albums[2], albums[3], albums[4]]
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,recommendations=recommendations)
        elif request.form['show_type'] == 'Songs': # if the Songs radio button was selected
            print("Songs")
            tracks = track.get_track((request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            user_choice = request.form['show_type']
            recommendations = [tracks[0], tracks[1], tracks[2], tracks[3], tracks[4]]
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,recommendations=recommendations)

    else: # If user visits the page
        return render_template('home_page.html')
    
@app.route('/other_page')
def search_page():
    return render_template('search_page.html')


if __name__ == "__main__":
    app.run(debug=True, port = 8000)
