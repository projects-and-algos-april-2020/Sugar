from flask import flash
from sqlalchemy.sql import func
from config import db, bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
INVALID_PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$')

requests = db.Table("requests",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="cascade"), primary_key=True),
    db.Column("item_id", db.Integer, db.ForeignKey("items.id", ondelete="cascade"), primary_key=True))


class Users(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255))
    email=db.Column(db.String(255))
    password_hash=db.Column(db.String(255))
    created_at=db.Column(db.DateTime, server_default=func.now())
    updated_at=db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_reqeusts = db.relationship("Items",
    secondary=requests,
    passive_deletes=True)
    @classmethod
    def create_request(cls, data):
        user = Users.query.get(data["user_Pd"])
        item = Items.query.get(data["item_id"])
        user.user_reqeusts.append(item)
        db.session.commit()

    @classmethod
    def validate_user(cls, data):
        valid = True
        if len(data["email"])<1:
            valid=False
            flash("email required!")
        else:
            if not EMAIL_REGEX.match(data["email"]):
                valid = False
                flash("invalid email")
        if len(data["username"])<1:
            valid=False
            flash("username required!")
        if len(data["password"])<1:
            valid=False
            flash("password required!")
        if len(data["password"])<8:
            valid=False
            flash("password must be at least eight characters!")
        else:
            if data["password"]!=data["confirm_password"]:
                valid=False
                flash("passwords do not match!")
            else:
                if INVALID_PASSWORD_REGEX.match(data["password"]):
                    valid = False
                    flash("password requires one uppercase, one number.")
        return valid 
    @classmethod
    def validate_user_login(cls, data):
        user = Users.query.filter_by(username=data["username"]).first()
        valid = True
        if len(data["username"])<1:
            valid=False
            flash("username required")
        if len(data["password"])<1:
            valid=False
            flash("password required")
        else:
            if not bcrypt.check_password_hash(user.password_hash, data["password"]):
                valid=False
                flash("password invalid!")
        return valid
    @classmethod
    def add_user(cls, data):
        password_hash = bcrypt.generate_password_hash(data["password"])
        new_user = cls(
            username=data["username"], 
            email=data["email"], 
            password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    @classmethod
    def display_user(cls, data):
        user = Users.query.filter_by(username=data["username"]).first()
        return user

class Categories(db.Model):
    __tablename__="categories"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    @classmethod
    def display_categories(cls):
        categories = Categories.query.all()
        return categories

class Items(db.Model):
    __tablename__="items"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(255))
    category_id=db.Column(db.Integer, 
        db.ForeignKey("categories.id", ondelete="cascade"),
        nullable=False)
    category = db.relationship("Categories",
        foreign_keys=[category_id],
        backref="posts",
        cascade="all")



