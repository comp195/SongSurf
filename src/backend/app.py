# How to Run
    # 1) Enter src/backend directory

    # 2) Activate database

    # 3) Activate website
        # unix> python3 app.py
        # windows> python app.py

import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
with app.app_context():
    db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True) # User_ID Column
    song_favorites = db.Column(db.String(300), nullable=False) # Song Favorites Column
    artist_favorites = db.Column(db.String(300), nullable=False) # Artist Favorites Column
    album_favorites = db.Column(db.String(300), nullable=False) # Album Favorites Column

    def __repr__(self):
        return '<User_id %r>' % self.user_id

@app.route('/', methods=['POST', 'GET']) # Methods are used in if statements below
def index():
    if request.method == 'POST': # If use clicks 'SURF', then bring them to song reccomended page
        #aas_search = [] # array to store "album_artist_song_search" values
        #aas_search.append(request.form['content'])
        #print(aas_search)
        return render_template('reccomend_page.html')
    else:
        return render_template('index.html')


    


if __name__ == "__main__":
    app.run(debug=True)
