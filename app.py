from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from datetime import datetime
import hashlib
import logging
import sqlite3


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SECRET_KEY'] = 'mysecret'
logging.basicConfig(filename='access_flask.log',level=logging.DEBUG)

db = SQLAlchemy(app)

class Person(db.Model): # This is one table
    id = db.Column(db.Integer, primary_key=True) # This is column 1
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    tw_id = db.Column(db.String(30))


class PersonView(ModelView):
    # Show only name and email columns in list view
    
    column_list = ('name', 'email', 'tw_id')
    form_columns = (
        'name',
        'email',
    )
    def on_model_change(self, form, model, is_created): # TO add entries to db without taking user input.. we can do calculation here
        model.tw_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()
        pass

class Triggered(db.Model): # This is one table
    id = db.Column(db.Integer, autoincrement=True) # This is column 1
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    tw_id = db.Column(db.String(100), primary_key=True)
    remote_host = db.Column(db.String(100))
    request_time = db.Column(db.String(100))
    
class TriggeredView(ModelView):
    can_create = False
    can_edit = False
    can_delete = True
    column_list = ('name', 'email', 'tw_id', 'remote_host', 'request_time')
    
    


@app.route("/rest")
def hello():
    return "HellO!"


    #https://blog.rizauddin.com/2008/04/python-parse-apache-log-to-sqlite_3548.html
    # https://pypi.org/project/pygtail/
   # https://stackoverflow.com/questions/17092697/select-same-column-from-multiple-tables-only-where-something-something
if __name__ == '__main__':
    admin = Admin(app)
    admin.add_view(PersonView(Person, db.session))
    admin.add_view(TriggeredView(Triggered, db.session))
    app.run(debug=True)
