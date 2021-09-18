from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import app, db
from .models import Todo, User


@app.route("/")
def main():
    return redirect(url_for("log_in"))


@app.route("/list")
@login_required
def index():
    todo_list = Todo.query.all()
    list = []
    for task in todo_list:
        for user in task.users:
            if user.id == current_user.id:
                list.append(task)
    return render_template("todo_list.html", todo_list=list)


@app.route("/add/task")
def add_task():
    return render_template("add_task.html")


@app.route("/add/task", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    author = User.query.filter(User.login == current_user.login).first()
    new_task = Todo(title=title, description=description, complete=False, author=author)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("add_task"))


@app.route("/edit/task/<int:pk>")
def edit_task(pk):
    task = Todo.query.get(pk)
    return render_template("edit_task.html", task=task)


@app.route("/edit/<int:pk>", methods=["POST"])
def edit(pk):
    task = Todo.query.get(pk)
    new_title = request.form.get("title")
    if new_title and new_title != task.title:
        task.title = new_title
    new_description = request.form.get("description")
    if new_description and new_description != task.description:
        task.description = new_description
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:pk>")
def update(pk):
    todo = Todo.query.filter_by(id=pk).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:pk>")
def delete(pk):
    todo = Todo.query.filter_by(id=pk).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def log_in():
    login = request.form.get("login")
    password = request.form.get("password")

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Login or password is incorrect")
    else:
        flash("Please fill login and password fields")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    login = request.form.get("login")
    password = request.form.get("password")
    password2 = request.form.get("password2")

    if request.method == "POST":
        if not (login or password or password2):
            flash("Please, fill all the fields")
        elif password != password2:
            flash("Passwords are not equal")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("log_in"))

    return render_template("register.html")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("log_in"))

