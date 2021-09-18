from flask_login import UserMixin, current_user

from . import db, manager


todos = db.Table(
    "todos",
    db.Column("todo_id", db.Integer, db.ForeignKey("todo.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.String(250))
    complete = db.Column(db.Boolean())

    def __init__(self, title, description, complete, author):
        self.title = title
        self.description = description
        self.complete = complete
        self.users = []
        author = User.query.filter(User.login == current_user.login).first()
        self.users.append(author)

    def __str__(self):
        return self.title


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    tasks = db.relationship(Todo, secondary=todos, lazy="subquery", backref="users")


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
