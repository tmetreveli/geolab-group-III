from flask import Flask, render_template, request, redirect, flash, url_for, session
from forms import AddDogForm, RegisterForm, LoginForm
import os
from models import Dog, User, Product, Comment
from configs import app, db
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests

@app.route('/')
def index():
    comments = Comment.query.all()
    for comment in comments:
        print(comment)
    comment_by_first_user = Comment.query.filter_by(user_id=2)
    print("------------------")
    for comment in comment_by_first_user:
        print(f"type: {type(comment.product)}")
        print(f"{comment}: ----- {comment.product.name}")

    print("------------------")
    products = Product.query.all()
    for product in products:
        for comment in product.comments:
            print(f"{product.name}: - {comment}")
    dogs = Dog.query.all()

    return render_template('about.html', dogs=dogs)


@app.route("/detailed_info/<int:dog_id>")
@login_required
def detailed_info(dog_id):

    selected_dog = Dog.query.get(dog_id)
    print(selected_dog)
    return render_template("dog_details.html", dog=selected_dog)

@app.route("/add_dog", methods=["GET", "POST"])
@login_required
def add_dog():
    form = AddDogForm()
    if request.method == "POST":
        file = request.files['img']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # dog = {"name": form.name.data, "img": filename, "description": form.description.data, "id":len(dogs)}
        # dogs.append(dog)
        dog = Dog(name=form.name.data, img=filename, description=form.description.data)
        db.session.add(dog)
        db.session.commit()
        return redirect("/")
    return render_template("add_dog.html", form=form)


@app.route("/edit_dog/<int:id>", methods=["GET", "POST"])
@login_required
def edit_dog(id):
    selected_dog = Dog.query.get(id)
    form = AddDogForm(name=selected_dog.name, img=selected_dog.img, description=selected_dog.description)
    print(selected_dog)
    if request.method == "POST":
        file = request.files['img']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        selected_dog.name = form.name.data
        selected_dog.img = filename
        selected_dog.description = form.description.data
        db.session.commit()
        return redirect("/")
    return render_template("add_dog.html", form=form)

@app.route("/delete_dog/<int:id>", methods=["GET", "POST"])
@login_required
def delete(id):
    deleted_dog = Dog.query.get(id)
    db.session.delete(deleted_dog)
    db.session.commit()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("თქვენ წარმატბეით გაიარეთ რეგისტრაცია")
        return redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
    # მოვძებნოთ user და შევამოწმოთ პაროლი
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია")
            return redirect("/")
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("თქვენ გამოხვედით საიტიდან")
    return redirect("/")


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    product = Product.query.get_or_404(product_id)

    # Handle comment submission
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You must be logged in to leave a comment!")
            return redirect(url_for('login'))

        content = request.form['content']
        if not content:
            flash("Comment cannot be empty!")
            return redirect(url_for('product_page', product_id=product_id))

        comment = Comment(content=content, user_id=current_user.id, product_id=product_id)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added successfully!")
        return redirect(url_for('product_page', product_id=product_id))

    return render_template('product_page.html', product=product)

@app.route("/api")
def api_route():
    api = "https://fakestoreapi.com/products"
    data = requests.get(api)
    print(data)

"""
CRUD - Create Retrieve Update Delete
"""