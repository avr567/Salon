import datetime
import os
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from sqlalchemy import and_
from models import db, Patron, Owner, Appointment, OpenAppointment, Stylist

app = Flask(__name__)
app.secret_key = "this is a terrible secret key"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'salon.db')
DEBUG = True

app.config.from_object(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.cli.command('initdb')
def initdb_command():

    """Reinitializes the database"""
    db.drop_all()
    db.create_all()
    # populate users
    db.session.add(Owner("owner", "pass"))

    db.session.commit()
    print('Initialized the database.')




@app.route("/")
def default():

	return redirect(url_for("logger"))

@app.route("/login/", methods=["GET", "POST"])
def logger():
    if "username" in session:
        owner = Owner.query.filter_by(username=session["username"]).first()
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        if owner is not None:
            return redirect(url_for("own"))
        elif stylist is not None:
            return redirect(url_for("style", username=session["username"]))
        elif patron is not None:
            return redirect(url_for("pat", username=session["username"]))
    elif request.method == "POST":
        name = request.form["username"]
        passy = request.form["password"]
        owner = Owner.query.filter_by(username=name).first()
        stylist = Stylist.query.filter_by(username=name).first()
        patron = Patron.query.filter_by(username=name).first()
        
        
        
        if owner is not None:
        
            if owner.password == passy:
                session["username"] = name
                flash('logged in')
                return redirect(url_for("own"))
            else:
                flash('invalid password')
        elif stylist is not None:
        
            if stylist.password == passy:
                session["username"] = name
                flash('logged in')
                return redirect(url_for("style", username=session["username"]))
            else:
                flash('invalid password')
        elif patron is not None:
        
            if patron.password == passy:
                flash('logged in')
                session["username"] = name
                return redirect(url_for("patronStyle", username=None))
            else:
                flash('invalid password')
        else:
            flash('username or password incorrect')
                
    return render_template('login.html')
	

@app.route("/register/", methods=["GET", "POST"])
def reg():
    if "username" in session:
        owner = Owner.query.filter_by(username=session["username"]).first()
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        
        if owner is not None:
            return redirect(url_for("own"))
        elif stylist is not None:
            return redirect(url_for("style", username=session["username"]))
        elif patron is not None:
            return redirect(url_for("pat", username=session["username"]))

    elif request.method == "POST":
        name = request.form["username"]
        passy = request.form["password"]
        owner = Owner.query.filter_by(username=name).first()
        stylist = Stylist.query.filter_by(username=name).first()
        patron = Patron.query.filter_by(username=name).first()
        
        if owner is not None:
            flash('username not available')
            return render_template('register.html')
            
        elif stylist is not None:
            flash('username not available')
            return render_template('register.html')
        elif patron is not None:
            flash('username not available')
            return render_template('register.html')
        else:
            flash('patron account registered')
            db.session.add(Patron(name, passy))
            db.session.commit()
            return redirect(url_for("logger"))
    
	
    return render_template('register.html')

	
@app.route("/owner/")
def own():
    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        
        if stylist is not None:
            abort(403)
        elif patron is not None:
            abort(403)

        stylists = Stylist.query.all()
        return render_template('owner.html', stylists=stylists)
    abort(403)
	


@app.route("/owner/stylists/")
@app.route("/owner/stylists/<username>/")
def ownerStyle(username=None):
    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        
        if stylist is not None:
            abort(403)
        elif patron is not None:
            abort(403)
        if username == None:
            return redirect(url_for("own"))
        if Stylist.query.filter_by(username=username).first() == None:
            return redirect(url_for("own"))
        stylist = Stylist.query.filter_by(username=username).first()
        return render_template('owner-stylist.html', username=stylist)
    abort(403)

    

@app.route("/owner/patrons/")
@app.route("/owner/patrons/<username>/")
def ownerPatron(username=None):
    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        
        if stylist is not None:
            abort(403)
        elif patron is not None:
            abort(403)
        if username == None:
            return redirect(url_for("own"))
        if Patron.query.filter_by(username=username).first() == None:
            return redirect(url_for("own"))
        patron = Patron.query.filter_by(username=username).first()
        return render_template('owner-patron.html', username=patron)
    abort(403)

@app.route("/registerStylists/", methods=["GET", "POST"])
def createStyle():
    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        
        
        if stylist is not None:
            abort(403)
        elif patron is not None:
            abort(403)
            
        if request.method == "POST":
            name = request.form["username"]
            passy = request.form["password"]
            owner = Owner.query.filter_by(username=name).first()
            stylist = Stylist.query.filter_by(username=name).first()
            patron = Patron.query.filter_by(username=name).first()
            
            if owner is not None:
                flash("username not available")
                stylists = Stylist.query.all()
                return render_template('owner.html', stylists=stylists )
            elif stylist is not None:
                flash("username not available")
                stylists = Stylist.query.all()
                return render_template('owner.html', stylists=stylists )
            elif patron is not None:
                flash("username not available")
                stylists = Stylist.query.all()
                return render_template('owner.html', stylists=stylists )
            else:
                db.session.add(Stylist(name, passy))
                for x in range(7):
                    temp = datetime.date.today() + datetime.timedelta(days=x)
                    if temp.weekday() == 6 or temp.weekday() == 0:
                        continue
                    for y in range (8):
                        db.session.add(OpenAppointment(name, temp, str(y+1) + " pm"))
                    for z in range(2):
                        db.session.add(OpenAppointment(name, temp, str(z+10) + " am"))
                    db.session.add(OpenAppointment(name, temp, "12 pm"))
                db.session.commit()
                flash('stylist created')
                return redirect(url_for("logger"))
	
        return render_template('register-stylist.html')
    abort(403)

@app.route("/stylist/")
def style():
    if "username" in session:
        owner = Owner.query.filter_by(username=session["username"]).first()
        patron = Patron.query.filter_by(username=session["username"]).first()
        
        if owner is not None:
            abort(403)
        elif patron is not None:
            abort(403)

        stylist = Stylist.query.filter_by(username=session["username"]).first()
        return render_template('stylist.html', username=stylist)
	
    abort(403)
	

@app.route("/patron/", methods=["GET", "POST"])
def pat():
    if "username" in session:
            owner = Owner.query.filter_by(username=session["username"]).first()
            stylist = Stylist.query.filter_by(username=session["username"]).first()
            
            if owner is not None:
                abort(403)
            elif stylist is not None:
                abort(403)

            patron = Patron.query.filter_by(username=session["username"]).first()
            
            return render_template('patron.html', username=patron)
        
    abort(403)
    
	
@app.route("/patron/stylists/")
@app.route("/patron/stylists/<username>/")
def patronStyle(username=None):

    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        owner = Owner.query.filter_by(username=session["username"]).first()
        
        
        if stylist is not None:
            abort(403)
        elif owner is not None:
            abort(403)
        if username == None:
            stylists = Stylist.query.all()
            return render_template('patron-stylists.html', username=None, stylists=stylists)
        else:
            stylist = Stylist.query.filter_by(username=username).first()
            return render_template('patron-stylists.html', username=stylist, stylists=None)
            
            
    abort(403)

@app.route("/appointment/<username>/<date>/<time>")
def appoint(username=None, date=None, time=None):
    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        owner = Owner.query.filter_by(username=session["username"]).first()
        if stylist is not None:
            abort(403)
        elif owner is not None:
            abort(403)
        if username == None or date == None or time == None:
            return redirect(url_for("pat"))

        db.session.add(Appointment(username, session["username"], date, time))
        appointments = OpenAppointment.query.filter_by(time=time).all()
        for x in appointments:
            if x.stylist_username == username and date == x.date:
                db.session.delete(x)
        
        db.session.commit()
        flash('appointment created')
        return redirect(url_for("pat"))
        
    abort(403)
    

     
@app.route("/cancel/<username>/<date>/<time>")
def can(username=None, date=None, time=None):
    if "username" in session:
        stylist = Stylist.query.filter_by(username=session["username"]).first()
        owner = Owner.query.filter_by(username=session["username"]).first()
        if stylist is not None:
            abort(403)
        elif owner is not None:
            abort(403)
        if username == None or date == None or time == None:
            return redirect(url_for("pat"))

        db.session.add(OpenAppointment(username, date, time))
        appointments = Appointment.query.filter_by(time=time).all()
        for x in appointments:
            if x.stylist_username == username and x.date == date:
              
                db.session.delete(x)
        db.session.commit()
        flash('appointment cancelled')
        return redirect(url_for("pat"))
    abort(403)
    
@app.route("/logout/")
def unlogger():
    if "username" in session:
        session.clear()
        flash('logged out')
        return redirect(url_for("logger"))
    else:
        return redirect(url_for("logger"))
        
			
if __name__ == "__main__":
    app.run()