# run this script to create the database if not already existings within 'instance'
from app import app, db
app.app_context().push()
db.create_all()