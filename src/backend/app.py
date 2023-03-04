# How to Run
    # Enter src/backend directory
    # Enter command
        # unix> python3 app.py
        # windows> python app.py

import os
from flask import Flask, render_template, url_for

template_dir = os.path.abspath('../frontend/templates')
app = Flask(__name__, static_folder='../frontend/static', template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
