from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patron(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, nullable=False)
	password = db.Column(db.Text, nullable=False)
	appointments = db.relationship('Appointment', backref = 'patron',lazy='dynamic')
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
	
class Owner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.Text, nullable=False)
	password = db.Column(db.Text, nullable=False)
	
	def __init__(self, username, password):
		self.username = username
		self.password = password

class Stylist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    appointments = db.relationship('Appointment', backref = 'stylist',lazy='dynamic')
    open_appointments = db.relationship('OpenAppointment', backref = 'stylist',lazy='dynamic')
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stylist_username = db.Column(db.Text, db.ForeignKey(Stylist.username), nullable=False)
    patron_username = db.Column(db.Text, db.ForeignKey(Patron.username), nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)
    def __init__(self, stylist_username, patron_username, date, time):
        self.stylist_username = stylist_username
        self.patron_username = patron_username
        self.date = date
        self.time = time
        
        
        
class OpenAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stylist_username = db.Column(db.Text, db.ForeignKey(Stylist.username), nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    def __init__(self, stylist_username, date, time):
        self.stylist_username = stylist_username
        self.date = date
        self.time = time