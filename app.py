from distutils.command.sdist import sdist
from enum import unique
from genericpath import exists
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask import Flask, redirect, render_template, session, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey, select
from datetime import datetime
import sqlite3
import os
from flask import g, send_from_directory
from flask_login import login_required, login_user, current_user, login_manager, logout_user, UserMixin, LoginManager




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'sdafwer3rw93ur9wu0er339de'

admin = Admin(app, url = '/sakjhfajsewdsjasfe')
#sakjhfajsewdsjasfe

      
class Forms(db.Model):  
    __tablename__ = 'forms'  
    id = db.Column(db.Integer, primary_key = True)  
    names = db.Column(db.String(200), nullable = False)
    emails = db.Column(db.String(200), unique = False)
    team_name_id = db.Column(db.Integer, db.ForeignKey('team_names.id'))
    
    def __repr__(self):
        return '<Forms %r>' % self.id
    
    def __init__(self, names, emails, team_names):
        self.names = names
        self.emails = emails
        self.team_names = team_names


                
class Team_names(db.Model):
    __tablename__ = 'team_names'
    id = db.Column(db.Integer, primary_key = True)
    team_name = db.Column(db.String(200), unique = True)
    formss = db.relationship('Forms', backref = 'team_names', lazy=True)  
    def __repr__(self):
        return '<Team_names %r>' % self.id

    def __init__(self, team_name):
        self.team_name = team_name  


admin.add_view(ModelView(Forms, db.session))
admin.add_view(ModelView(Team_names, db.session))




  

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/icon.png')

    
@app.route('/starthere', methods=['POST','GET'])
def first():
    return render_template('first.html')

@app.route('/new', methods=['POST','GET'])
def new():
    if request.method == 'POST':
        givenname = request.form['names']
        givenemail = request.form['emails']
        giventeamnames = request.form['team_names']
        
        adding1 = Team_names(team_name = giventeamnames)
        adding = Forms(names = givenname, emails = givenemail, team_names=adding1) 
        
        
        try: 
            
            db.session.add(adding)
            db.session.add(adding1)
            db.session.commit()
            return render_template('thankyou.html')
        except: 
            return render_template('fail1.html')
    else:
        return render_template('new.html')

@app.route('/join', methods=['POST','GET'])   
def join():
   
    teams = Team_names.query.with_entities(Team_names.team_name)
    for team in teams:
       team = Team_names.team_name
       
    

    if request.method == 'POST':
    
        givennames = request.form['names']   
        givenemails = request.form['emails']
        select = request.form.get("selected")   
        selected_team = db.session.query(Team_names).filter(Team_names.team_name == select).first()
        adding = Forms(names = givennames, emails = givenemails, team_names = selected_team)        
        
        try: 
            
            db.session.add(adding)    
            db.session.commit()
            return render_template('thankyou.html')   
        except:
            return render_template('fail2.html')
             
    else:
        return render_template("join.html", teams=teams)  

if __name__ == "__main__":
    app.run(debug=True)

