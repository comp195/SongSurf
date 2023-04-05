import os
import logging
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy



import artist as artist
import album 
import track

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
# Specify the full path of the database file
DB_FILEPATH = os.path.join(os.path.dirname(__file__), 'instance', 'main.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILEPATH}' # configure database

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s')


print("* Running on http://127.0.0.1:8000")

# initialize database and import the needed database objects
from database import init_db, User
db = init_db(app)

#use this code to reset database
# with app.app_context():
#     # reset database
#     db.drop_all()
#     db.create_all()

# Define route for main page (search_page)
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
        
        # Create a new User object with the AAS searches and add it to the database
        new_user = User(email='test1@pacific.edu', password='uop1') # temporarily make email and password the same for all users created
        try:
            db.session.add(new_user)
            db.session.commit()
            app.logger.info('Successfully added user')
        except Exception as e:
            app.logger.error('Issue adding user. Error: %s', str(e))
            print(e)

          # If artists were chosen, treat user input as all artists, etc.
        if request.form['show_type'] == 'Artists':	# if the Artists radio button was selected
            print("Artists")
            artists = artist.get_artist(request.form['user_choice1'], request.form['user_choice2'], request.form['user_choice3'])
            if not artists:	# if tracks is empty
                error_message = "No tags were able to be found for any of the artists.  Please try other songs."
                return render_template('search_page.html', message=error_message)
            user_choice = request.form['show_type']
            recommendations = [artists[0], artists[1], artists[2], artists[3], artists[4]]
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,recommendations=recommendations)
        elif request.form['show_type'] == 'Albums': # if the Albums radio button was selected
            print("Albums")
            albums = album.get_album((request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            if not albums:	# if albums is empty
                error_message = "No tags were able to be found for any of the albums.  Please try other songs."
                return render_template('search_page.html', message=error_message)
            user_choice = request.form['show_type']
            recommendations = [albums[0], albums[1], albums[2], albums[3], albums[4]]
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,recommendations=recommendations)
        elif request.form['show_type'] == 'Songs': # if the Songs radio button was selected
            print("Songs")
            tracks = track.get_track((request.form['user_choice1'],request.form['user_choice4']), (request.form['user_choice2'],request.form['user_choice5']), (request.form['user_choice3'],request.form['user_choice6']))
            if not tracks:	# if tracks is empty
                error_message = "No tags were able to be found for any of the tracks.  Please try other songs."
                return render_template('search_page.html', message=error_message)
            user_choice = request.form['show_type']
            recommendations = [tracks[0], tracks[1], tracks[2], tracks[3], tracks[4]]
            return render_template('reccomend_page.html', user=new_user, user_choice = user_choice,recommendations=recommendations)

    else: # If user visits the page
        return render_template('home_page.html')
    
@app.route('/other_page')
def search_page():
    return render_template('search_page.html')

@app.route('/home_page')
def home_page():
    return render_template('home_page.html')


if __name__ == "__main__":
    app.run(debug=True, port = 8000) # when deployed, set debug=False
