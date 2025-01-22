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
    category = request.form.get("category") #Gets task categories
    new_todo = Todo(task=task, category = category)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("my_view.home")) 

@my_view.route("/update/<todo_id>", methods = ["POST"])
def update(todo_id):
    todo = Todo.query.filter_by(id = todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
#Next 3 lines redirect the user to the same page after update
    category = request.args.get("category")
    if category:
        return redirect(url_for("my_view.category", category_name = category))
    return redirect(url_for("my_view.home")) #Redirects to home page if no category has been specified

@my_view.route("/delete/<todo_id>", methods = ["GET"])
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()

    category = request.args.get("category")
    if category:
        return redirect(url_for("my_view.category", category_name = category))
    return redirect(url_for("my_view.home"))

#Route that enables editing of the specified task by its identification (Primary key)
@my_view.route("/edit/<todo_id>", methods = ["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() #Queries db for the task with the specified primary key
    if not todo:
        return "Todo not found", 404 #If said task does not exist, it will return a 404 error, also known as "Not Found"
#Capture the category from the query string
    category = request.args.get("category") 
    
    if request.method == "POST": #Method that handles the POST request to update the identified task
        new_task = request.form.get("task") #Gets the edited task from the edit.html form
        todo.task = new_task #Appends the edited task in the database
        category = request.form.get("category")#Gets category from the form
        db.session.commit() #Commits task changes to the database

        #Capture the origin category
        origin_category = request.form.get("origin_category")
    #Redirects to the category page if provided - POST
        if origin_category:
            return redirect(url_for("my_view.category", category_name = origin_category))  #renders the edit.html form, and passes the edited task to the specific category page. 
        return redirect(url_for("my_view.home")) #renders the edit.html form, and passes the edited task to homepage.
#For GET requests
    return render_template("edit.html", todo=todo, category=category)

#Filter tasks by their specifically assigned category
@my_view.route("/category/<category_name>")
def category(category_name):
    todo_list = Todo.query.filter_by(category = category_name).all() #Will get tasks by assigned category to them
    return render_template("category.html", todo_list = todo_list, category_name = category_name)