from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import Todo
from . import db
my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list = todo_list)

@my_view.route("/add", methods = ["POST"])
def add():
    task = request.form.get("task")
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("my_view.home")) 

@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))

#Route that enables editing of the specified task by its identification (Primary key)
@my_view.route("/edit/<todo_id>", methods = ["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() #Queries db for the task with the specified primary key
    if not todo:
        return "Todo not found", 404 #If said task does not exist, it will return a 404 error, also known as "Not Found"
    
    if request.method == "POST": #Method that handles the POST request to update the identified task
        new_task = request.form.get("task") #Gets the edited task from the edit.html form
        todo.task = new_task #Appends the edited task in the database
        db.session.commit() #Commits task changes to the database
        return redirect(url_for("my_view.home")) #redirects user back to the homepage once user has pressed "Save Changes"
    
    return render_template("edit.html", todo=todo) #renders the edit.html form, and passes the task to this template.