from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin import BaseView, expose
from datetime import datetime
import hashlib
import logging
import sqlite3
from flask_admin.helpers import get_form_data
from flask_admin.babel import gettext
from markupsafe import Markup
from flask import redirect, flash, url_for
import payload

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SECRET_KEY'] = 'mysecret'
logging.basicConfig(filename='access_flask.log',level=logging.DEBUG)

db = SQLAlchemy(app)

class Tripwires(db.Model): # This is one table
    id = db.Column(db.Integer, primary_key=True) # This is column 1
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tw_id = db.Column(db.String(30))
    desc = db.Column(db.String(300))
    priority = db.Column(db.Integer)
    payload = db.Column(db.String(50))

class TripwiresView(ModelView):
    # Show only name and email columns in list view
    
    column_list = ('name', 'email', 'desc', 'priority', 'tw_id', 'payload', 'Download Payload')
    form_columns = (
        'name',
        'email',
        'desc',
        'priority',
        'payload'
    )
    form_choices = { 'priority': [ ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                     'payload': [('Email', 'Email'), ('Image', 'Image'),('MS Word', 'MS Word'),('Windows bat', 'Windows bat'),('Linux Executable', 'Linux Executable'), ('robots.txt', 'robots.txt'),('secrets.pdf', 'secrets.pdf')]
                   }
    column_labels = {
        'desc': 'Description',
        
    }
    def on_model_change(self, form, model, is_created): # TO add entries to db without taking user input.. we can do calculation here
        model.tw_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()
        pass

    # Form for Download payload buttton

    def _format_pay_now(view, context, model, name):

        # render a form with a submit button for student, include a hidden field for the student id                          
        # note how checkout_view method is exposed as a route below                                                          
        checkout_url = url_for('.checkout_view')

        _html = '''
            <form action="{checkout_url}" method="POST">
                <input id="id" name="id"  type="hidden" value="{id}">
                <button type='submit'>Download</button>
            </form
        '''.format(checkout_url=checkout_url, id=model.id)

        return Markup(_html)
    column_formatters = {
        'Download Payload': _format_pay_now
    }

    @expose('checkout', methods=['POST'])
    def checkout_view(self):

        return_url = self.get_url('.index_view')
        print(return_url)
        form = get_form_data()

        if not form:
            flash(gettext('Could not get form from request.'), 'error')
            return redirect(return_url)

        # Form is an ImmutableMultiDict
        id = form['id']
        print(id)
        # Get the model from the database
        model = self.get_one(id)

        if model is None:
            flash(gettext('Student not not found.'), 'error')
            return redirect(return_url)

        # process the model
        model.is_paid = True

        try:
            payload.download(id)
            flash(gettext('Student, ID: {id}, set as pajshagfjshdfgjsdfgsdjhfgid'.format(id=id)))
            
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to set student, ID: {id}, as paid'.format(id=id), error=str(ex)), 'error')

        return redirect(return_url)
class Triggered(db.Model): # This is one table
    id = db.Column(db.Integer, autoincrement=True) # This is column 1
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    tw_id = db.Column(db.String(100), primary_key=True)
    desc = db.Column(db.String(300))
    priority = db.Column(db.Integer)
    payload = db.Column(db.String(50))
    remote_host = db.Column(db.String(100))
    request_time = db.Column(db.String(100))
    
class TriggeredView(ModelView):
    can_create = False
    can_edit = False
    can_delete = True
    column_list = ('name', 'email', 'desc', 'priority', 'payload', 'remote_host', 'request_time')


class ExportView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/export.html')


@app.route("/rest")
def hello():
    return "HellO!"


    #https://blog.rizauddin.com/2008/04/python-parse-apache-log-to-sqlite_3548.html
    # https://pypi.org/project/pygtail/
   # https://stackoverflow.com/questions/17092697/select-same-column-from-multiple-tables-only-where-something-something
if __name__ == '__main__':
    admin = Admin(app)
    admin.add_view(TripwiresView(Tripwires, db.session))
    admin.add_view(TriggeredView(Triggered, db.session))
    admin.add_view(ExportView(name='Export', endpoint='export'))
    app.run(debug=True)
