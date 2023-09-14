from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class Venue(db.Model):
    __tablename__ = "venue"
    venue_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    Vname = db.Column(db.Unicode, nullable = False)
    place = db.Column(db.Unicode, nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    shows = db.relationship("Show", cascade="delete")

class Show(db.Model):
    __tablename__ = "show"
    __searchable__ = ['Sname']
    show_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    Sname = db.Column(db.Unicode, nullable = False)
    rating = db.Column(db.Float) 
    Tags = db.Column(db.Unicode)
    price = db.Column(db.Integer, nullable=False)
    timing = db.Column(db.DateTime)
    tickets_remaining = db.Column(db.Integer)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable=False)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     self.fs_uniquifier = str(self.id)
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    # name = db.Column(db.String)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    html_pdf = db.Column(db.String(255), default="HTML")


class Booking(db.Model):
    __tablename__ = "booking"
    booking_id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey("user.id"))
    # venue_id = db.Column(db.Integer, db.ForeignKey("Venue.venue_id"))
    show_id = db.Column(db.Integer, db.ForeignKey("show.show_id"))
    no_of_tickets = db.Column(db.Integer, nullable= False)
    rating = db.Column(db.Integer)
    booking_time = db.Column(db.DateTime, default=db.func.now())
    # Define the relationship to Show
    show = db.relationship("Show", backref="bookings")

    

