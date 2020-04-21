from flask import render_template, redirect, request, session, flash, session
from config import db, bcrypt, migrate
from models import Users, Categories, Items, Requests, Fulfilled
from sqlalchemy import desc

def index():
    return render_template('index.html')

def registerRequest():
    return render_template('partials/register.html')

def registerUser():
    valid = Users.validate_user(request.form)
    if not valid:
        return render_template('partials/errors.html')
    else:
        new_user=Users.add_user(request.form)
        session['user_id']=new_user.id
        session['username']=new_user.username
        return "success"

def loginRequest():
    return render_template('partials/login.html')

def loginUser():
    valid = Users.validate_user_login(request.form)
    if not valid:
        return render_template('partials/errors.html')
    else:
        print(request.form)
        user = Users.display_user(request.form)
        session['user_id']=user.id
        session['username']=user.username
        return "success"

def dashboard():
    requests = Requests.query.join(Requests.item).join(Requests.user).order_by(Requests.id.desc()).all()
    print(requests)
    return render_template('dashboard.html', requests=requests)

def item_list():
    category = request.form['category']
    category_items = Items.query.join(Items.category).filter_by(name=category).all()
    print(category)
    return render_template('partials/items_form.html', category_items=category_items)

def user_request():
    user = Users.query.get(session['user_id'])
    user_requests = Requests.query.join(Requests.item).join(Requests.user).filter_by(id=session['user_id']).all()
    print(user_requests)
    categories = Categories.display_categories()
    return render_template('requests.html', categories=categories, user_requests=user_requests)

def create_request():
    print(request.form)
    valid = Requests.submit_request(request.form)
    if not valid:
        return render_template('partials/errors.html')
    else:
        Requests.add_request(request.form)
        return "success"

def user_request_list():
    return render_template('partials/user_request_list.html')

def fulfill_request_form():
    print(request.form)
    users_list = Users.query.all()
    user_request = Requests.query.filter_by(id=request.form["request_id"]).first()
    return render_template('partials/fulfill_request.html', users_list=users_list, user_request=user_request)

def add_fulfilled():
    print(request.form)
    Fulfilled.add_fulfilled_request(request.form)
    return redirect('/request')