from datetime import datetime #Imports the datetime from datetime module
from Website import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(300), unique = True)
    complete = db.Column(db.Boolean, default = False)
    time_and_date = db.Column(db.DateTime, default=datetime.utcnow) #Adds the time and date column to Todo model, which stores the timestamp
    category = db.Column(db.String(50), default = "Other") #Sets category for tasks in database