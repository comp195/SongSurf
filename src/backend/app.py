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

# use this code to reset database
# with app.app_context():
#     # reset database
#     db.drop_all()
#     db.create_all()

# user_developer = User(first_name='dev', last_name='dev', username='dev', password='dev') # user credientials for developer
# with app.app_context():
#     db.session.add(user_developer)
#     db.session.commit()

#track.test_track(app)
#album.test_album(app)
#artist.test_artist(app)

# Define route for main page (home_page)
@app.route('/', methods=['POST', 'GET'])
def index():
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

        # ** use this code for registration page later on **
                # # Create a new User object with the AAS searches and add it to the database
                # new_user = User(email='test1@pacific.edu', password='uop1') # temporarily make email and password the same for all users created
                # try:
                #     db.session.add(new_user)
                #     db.session.commit()
                #     app.logger.info('Successfully added user')
                # except Exception as e:
                #     app.logger.error('Issue adding user. Error: %s', str(e))
                #     print(e)

          # If artists were chosen, treat user input as all artists, etc.
        if request.form['show_type'] == 'Artists':	# if the Artists radio button was selected
            print("Artists")

            # new implementation calling database instead
            database.delete_current_recommendations(app, user_id) # start with new recommendations since "SURF" is clicked
            artist.get_artist_recommendations(app, user_id, request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            artist_ids = database.get_artist_recommendations(app, user_id)
            artist_objects = [database.get_item_object_from_id(app, artist_id, 'artist') for artist_id in artist_ids]

            # old
            # artists = artist.get_artist_recommendations(app, request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            # if not artists:	# if tracks is empty
            #     error_message = "No tags were able to be found for any of the artists.  Please try other songs."
            #     return render_template('search_page.html', message=error_message)
            user_choice = request.form['show_type']
            return render_template('reccomend_page.html', user=user_id, user_choice = user_choice,recommendations=artist_objects)
        
        elif request.form['show_type'] == 'Albums': # if the Albums radio button was selected
            print("Albums")

            # new implementation calling database instead
            database.delete_current_recommendations(app, user_id) # start with new recommendations since "SURF" is clicked
            album.get_album_recommendations(app, user_id, (request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            album_ids = database.get_album_recommendations(app, user_id)
            album_objects = [database.get_item_object_from_id(app, album_id, 'album') for album_id in album_ids]
            artist_names = [database.get_name(app, album.artist_id, 'artist') for album in album_objects] 
            print(artist_names) # use this artist_names array later when clicking on a tile for more info of the album

            # old
            # albums = album.get_album_recommendations(app, (request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            # if not albums:	# if albums is empty
            #     error_message = "No tags were able to be found for any of the albums.  Please try other songs."
            #     return render_template('search_page.html', message=error_message)
            user_choice = request.form['show_type']
            return render_template('reccomend_page.html', user=user_id, user_choice = user_choice,recommendations=album_objects)
        
        elif request.form['show_type'] == 'Songs': # if the Songs radio button was selected
            print("Songs")

            # new implementation calling database instead
            database.delete_current_recommendations(app, user_id) # start with new recommendations since "SURF" is clicked
            track.get_track_recommendations(app, user_id, (request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            track_ids = database.get_track_recommendations(app, user_id)
            track_objects = [database.get_item_object_from_id(app, track_id, 'track') for track_id in track_ids]
            artist_names = [database.get_name(app, track.artist_id, 'artist') for track in track_objects] 
            print(artist_names) # use this artist_names array later when clicking on a tile for more info of the track

            # old
            # tracks = track.get_track_recommendations(app, (request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            # if not tracks:	# if tracks is empty
            #     error_message = "No tags were able to be found for any of the tracks.  Please try other songs."
            #     return render_template('search_page.html', message=error_message)
            user_choice = request.form['show_type']
            return render_template('reccomend_page.html', user=user_id, user_choice = user_choice,recommendations=track_objects)

    else: # If user visits the page
        return render_template('home_page.html', logged_in=False)
    
@app.route('/search_page')
def search_page():
    return render_template('search_page.html')

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



if __name__ == "__main__":
    app.run(debug=True, port = 8000) # when deployed, set debug=False
