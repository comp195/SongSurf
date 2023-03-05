# run this script to create the database if not already existings within 'instance'
from app import app, db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
with app.app_context():
    db.drop_all()
    db.create_all()

