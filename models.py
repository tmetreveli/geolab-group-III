"""
რელაციური - SQL და არარელაციური NOSQL- მონაცემთა ბაზები
Oracle, MSSQL, PostgreSQL, MySQL..., sqlite
"""
from flask_login import UserMixin
from configs import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class Dog(db.Model):
    name = db.Column(db.String(), nullable=False)
    img = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"{self.id}: {self.name}"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False, default="guest")

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='product', lazy=True)

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship('User', backref='comments')

    def __str__(self):
        return f"{self.user_id}: {self.content}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    dogs = [{"name": "pluto", "img": "dog1.jpeg", "description": "cute dog", "id": 0},
            {"name": "dog2", "img": "dog2.jpeg", "description": "excited", "id": 1},
            {"name": "jeka", "img": "dog3.jpeg", "description": "annoyed", "id": 2}]
    with app.app_context():
        db.create_all()
        for dog in dogs:
            new_dog = Dog(name=dog["name"], img=dog["img"], description=dog["description"])
            db.session.add(new_dog)
            db.session.commit()

        product = Product(name="Sample Product", description="This is a test product.")
        user = User(username="user", password="123")
        admin = User(username="admin", password="admin123", role="admin")
        db.session.add(user)
        db.session.add(admin)
        db.session.add(product)
        db.session.commit()

