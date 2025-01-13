from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func #adds usability for func.now() line 16

# new instance of the Flask class
app = Flask(__name__)

#Create crud operations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(300), unique = True)
    complete = db.Column(db.Boolean, default = False) 
    date_time = db.Column(db.DateTime, default=func.now()) #Sets date and time for created tasks automatically. Displayed time in index.html line 24. 

@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list = todo_list)

@app.route("/add", methods = ["POST"])
def add():
    task = request.form.get("task")
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home")) 

@app.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000) 