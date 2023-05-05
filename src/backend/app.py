import os
import logging
import database
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy



import artist as artist
import album 
import track

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
# Specify the full path of the database file
DB_FILEPATH = os.path.join(os.path.dirname(__file__), 'instance', 'main.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILEPATH}' # configure database
app.secret_key = 'stockton209' #Used for cookies

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')


print("* Running on http://127.0.0.1:8000")

# initialize database and import the needed database objects
from database import init_db, User
db = init_db(app)

# # use this code to reset database
# with app.app_context():
#     # reset database
#     db.drop_all()
#     db.create_all()

# user_developer = User(first_name='dev', last_name='dev', username='dev', password='dev') # user credientials for developer
# guest = User(first_name='guest', last_name='guest', username='guest', password='guest') # user credientials for guest
# with app.app_context():
#     db.session.add(user_developer)
#     db.session.add(guest)
#     db.session.commit()

#track.test_track(app)
#album.test_album(app)
#artist.test_artist(app)

# Define route for main page (home_page)
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('home_page.html', logged_in=False)

@app.route('/search_page', methods=['POST', 'GET'])
def search_page():
    if request.method == 'POST': # If user clicks SURF
        
         # Check if any input fields are empty
        if not request.form['user_choice1'] or not request.form['user_choice2'] or not request.form['user_choice3']:
            error_message = "Please fill out all three input fields."
            return render_template('search_page.html', message=error_message)

         # Check if any input fields are empty
        if (request.form['show_type'] == 'Albums' or request.form['show_type'] == 'Songs') and (not request.form['user_choice4'] or not request.form['user_choice5'] or not request.form['user_choice6']):
            error_message = "Please fill out all the artist input fields."
            return render_template('search_page.html', message=error_message)
        
        # Check if a radio button is selected
        if not request.form.get('show_type'):
            error_message = "Please select a category: Artists, Albums, or Songs"
            return render_template('search_page.html', message=error_message)

        # Check for unique inputs
        if (request.form['show_type'] == 'Artists'):
            all_choices = [request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3']]
        else:
            tuple1 = (request.form['user_choice1'], request.form['user_choice4'])
            tuple2 = (request.form['user_choice2'], request.form['user_choice5'])
            tuple3 = (request.form['user_choice3'], request.form['user_choice6'])

            all_choices = [tuple1, tuple2, tuple3]

        if len(all_choices) != len(set(all_choices)):
            error_message = "Please choose unique values for all input fields."
            return render_template('search_page.html', message=error_message)

        user_id = session.get('logged_in_user_id')
        if (user_id == None):
            user_id = 2    # Set to guest user
            session['logged_in_user_id'] = 2
        print(user_id)

        # If artists were chosen, treat user input as all artists, etc.
        if request.form['show_type'] == 'Artists':
            user_choice = request.form['show_type']
            recommendations = get_recommendations('artist', user_id, [request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3']])
            session['item_type'] = 'artist'
            if not recommendations:
                error_message = "Sorry, no recommended artists found. Please try other artists."
                return render_template('search_page.html', message=error_message)
            # Set recommendation = true
            for rec in recommendations:
                database.set_recommended(app, user_id, rec.artist_id, 'artist')
            return render_template('recommend_page.html', user=user_id, user_choice=user_choice, item_type='artist', recommendations=recommendations, artist_names=None)
        elif request.form['show_type'] == 'Albums':
            user_choice = request.form['show_type']
            recommendations, artist_names = get_recommendations('album', user_id, [request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'], request.form['user_choice4'], request.form['user_choice5'], request.form['user_choice6']])
            session['item_type'] = 'album'
            if not recommendations:
                error_message = "Sorry, no recommended albums found. Please try other albums."
                return render_template('search_page.html', message=error_message)
            return render_template('recommend_page.html', user=user_id, user_choice=user_choice, item_type='album', recommendations=recommendations, artist_names=artist_names)
        elif request.form['show_type'] == 'Tracks':
            user_choice = request.form['show_type']
            recommendations, artist_names = get_recommendations('track', user_id, [request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'], request.form['user_choice4'], request.form['user_choice5'], request.form['user_choice6']])
            session['item_type'] = 'track'
            if not recommendations:
                error_message = "Sorry, no recommended tracks found. Please try other tracks."
                return render_template('search_page.html', message=error_message)
            return render_template('recommend_page.html', user=user_id, user_choice=user_choice, item_type='track', recommendations=recommendations, artist_names=artist_names)
   
    else: # If user visits the page
        return render_template('search_page.html')
    
@app.route('/recommend_page', methods=['POST', 'GET'])
def recommend_page():
    print("recommend here")
    user_id = session.get('logged_in_user_id')
    print("user id = ")
    print(user_id)
    item_type = session.get('item_type')
    if request.method == 'POST':  # If a POST request is received (feedback submission)
        feedback = request.form.get('feedback')
        # Get original recommendations to display if like/dislike is clicked
        if item_type == 'artist':
            artist_ids = database.get_artist_recommendations(app, user_id)
            recommendations = [database.get_item_object_from_id(app, artist_id, 'artist') for artist_id in artist_ids][:3]
            artist_names = None
            favorite_ids = database.get_artist_likes(app, user_id)

        elif item_type == 'album':
            album_ids = database.get_album_recommendations(app, user_id)
            recommendations = [database.get_item_object_from_id(app, album_id, 'album') for album_id in album_ids][:3]
            artist_names = [database.get_name(app, album.artist_id, 'artist') for album in recommendations]
            favorite_ids = database.get_album_likes(app, user_id)

        elif item_type == 'track':
            track_ids = database.get_track_recommendations(app, user_id)
            recommendations = [database.get_item_object_from_id(app, track_id, 'track') for track_id in track_ids][:3]
            artist_names = [database.get_name(app, track.artist_id, 'artist') for track in recommendations]
            favorite_ids = database.get_track_likes(app, user_id)

        favorites = [database.get_item_object_from_id(app, item, item_type) for item in favorite_ids]
        
        if feedback == "like" or feedback == "dislike": # if like/dislike is clicked
            if (user_id == 2): # if guest
                guest_error_message = "Please make an account to get like or dislike music."
                print(guest_error_message)
                return render_template('recommend_page.html', user=user_id, item_type=item_type, recommendations=recommendations, artist_names=artist_names, favorites=favorites, guest_error_message=guest_error_message)
            feedback = request.form.get('feedback')
            rec_id = request.form.get('recId')
            print(feedback)
            print(rec_id)
            database.add_liked(app, user_id, rec_id, item_type)
            if item_type == 'artist':
                favorite_ids = database.get_artist_likes(app, user_id)
            if item_type == 'album':
                favorite_ids = database.get_album_likes(app, user_id)
            if item_type == 'track':
                favorite_ids = database.get_track_likes(app, user_id)
            favorites = [database.get_item_object_from_id(app, item, item_type) for item in favorite_ids]
            return render_template('recommend_page.html', user=user_id, item_type=item_type, recommendations=recommendations, artist_names=artist_names, favorites=favorites)


        if request.form.get('refresh_button'): # if refresh button is clicked, show more recommendations
            print("Clicked refresh")
            print(item_type)
            # If artists were chosen, treat user input as all artists, etc.
            if item_type == 'artist':
                for rec in recommendations: # Set recommendation = true
                    database.set_recommended(app, user_id, rec.artist_id, 'artist')
                artist_ids = database.get_artist_recommendations(app, user_id)
                recommendations = [database.get_item_object_from_id(app, artist_id, 'artist') for artist_id in artist_ids][:3]
                if not recommendations:
                    error_message = "No tags were able to be found for any of the artists.  Please try other artists."
                    return render_template('search_page.html', message=error_message)
                return render_template('recommend_page.html', user=user_id, user_choice='Artists', recommendations=recommendations, item_type='artist', favorites=favorites)

            elif item_type == 'album':
                for rec in recommendations: # Set recommendation = true
                    database.set_recommended(app, user_id, rec.album_id, 'album')
                album_ids = database.get_album_recommendations(app, user_id)
                recommendations = [database.get_item_object_from_id(app, album_id, 'album') for album_id in album_ids][:3]
                artist_names = [database.get_name(app, album.artist_id, 'artist') for album in recommendations]
                if not recommendations:
                    error_message = "No tags were able to be found for any of the albums.  Please try other albums."
                    return render_template('search_page.html', message=error_message)

                return render_template('recommend_page.html', user=user_id, user_choice='Albums', recommendations=recommendations, item_type='album', artist_names=artist_names, favorites=favorites)

            elif item_type == 'track':
                for rec in recommendations: # Set recommendation = true
                    database.set_recommended(app, user_id, rec.track_id, 'track')
                track_ids = database.get_track_recommendations(app, user_id)
                recommendations = [database.get_item_object_from_id(app, track_id, 'track') for track_id in track_ids][:3]
                artist_names = [database.get_name(app, track.artist_id, 'artist') for track in recommendations]
                if not recommendations:
                    error_message = "No tags were able to be found for any of the tracks.  Please try other tracks."
                    return render_template('search_page.html', message=error_message)
                return render_template('recommend_page.html', user=user_id, user_choice='Tracks', recommendations=recommendations, item_type='track', artist_names=artist_names, favorites=favorites)
        else:
            return render_template('recommend_page.html', user=user_id, item_type=item_type, recommendations=recommendations, artist_names=artist_names, favorites=favorites)
    else:
        return render_template('recommend_page.html', user=user_id, item_type=item_type, recommendations=recommendations, artist_names=artist_names, favorites=favorites)

@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

@app.route('/login_page', methods=['POST', 'GET'])
def login_page():
    print("login here")
    if request.method == 'POST': # if SIGN UP button is clicked
        # handle form submission here
        print("Check if valid username and password")
        username = request.form['username']
        password = request.form['password']
        print(username + password)
        if (database.check_if_valid_password(app, username, password) == False):
            invalid_message = "Incorrect username or password!"
            return render_template('login_page.html', invalid_message=invalid_message)
        
        logged_in_user_id = database.get_user_id(app, username)
        session['logged_in_user_id'] = logged_in_user_id
        return render_template('home_page.html', logged_in=True, username=username)
    else:
        return render_template('login_page.html')

@app.route('/signup_page', methods=['POST', 'GET'])
def signup_page():
    print("signup here")
    if request.method == 'POST': # if SIGN UP button is clicked
        # handle form submission here
        print("If valid user and password, then submit to database")
        fname = request.form['first_name']
        lname = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        print(fname + lname + username + password)
        # first check if username already exists
        if (database.add_user(app, fname, lname, username, password) == False or username == None):
            invalid_message = "That username already exists. Please enter a different one."
            return render_template('signup_page.html', invalid_message=invalid_message)
        new_user = User(first_name='dev', last_name='dev', username='dev', password='dev')
        return redirect('/login_page')
    else:
        return render_template('signup_page.html')


def get_recommendations(show_type, user_id, user_choices):
    # Delete current recommendations to start fresh
    database.delete_current_recommendations(app, user_id)

    if show_type == 'artist':
        # Get artist recommendations based on user choices
        artist.get_artist_recommendations(app, user_id, user_choices[0], user_choices[1], user_choices[2])
        artist_ids = database.get_artist_recommendations(app, user_id)
        artist_objects = [database.get_item_object_from_id(app, artist_id, 'artist') for artist_id in artist_ids][:3]

        return artist_objects

    elif show_type == 'album':
        # Get album recommendations based on user choices
        album.get_album_recommendations(app, user_id, (user_choices[0], user_choices[3]), (user_choices[1], user_choices[4]), (user_choices[2], user_choices[5]))
        album_ids = database.get_album_recommendations(app, user_id)
        album_objects = [database.get_item_object_from_id(app, album_id, 'album') for album_id in album_ids][:3]
        artist_names = [database.get_name(app, album.artist_id, 'artist') for album in album_objects]

        return album_objects, artist_names

    elif show_type == 'track':
        # Get track recommendations based on user choices
        track.get_track_recommendations(app, user_id, (user_choices[0], user_choices[3]), (user_choices[1], user_choices[4]), (user_choices[2], user_choices[5]))
        track_ids = database.get_track_recommendations(app, user_id)
        track_objects = [database.get_item_object_from_id(app, track_id, 'track') for track_id in track_ids][:3]
        artist_names = [database.get_name(app, track.artist_id, 'artist') for track in track_objects]

        return track_objects, artist_names



if __name__ == "__main__":
    app.run(debug=True, port = 8000) # when deployed, set debug=False
