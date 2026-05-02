from flask import (Flask, render_template, redirect, 
                   url_for)
from form import ContactForm
from flask_ckeditor import CKEditor
import sqlite3
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'

ckeditor = CKEditor(app)

# Connect to message.db in PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(BASE_DIR, "flask_ckeditor")

# Ensure folder exists
os.makedirs(db_dir, exist_ok=True)

# Full database path
db_path = os.path.join(db_dir, "message.db")

################# Route ##################
@app.route('/')
def index():
    form = ContactForm()
    return render_template('contact.html', form=form)

@app.route('/message', methods=['GET','POST'])
def submit():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subscribe = form.subscribe.data
        message = form.message.data
        
        # conn = sqlite3.connect("flask_ckeditor/message.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        try:
            query = """INSERT INTO message (name, email, subscribe, message)
               VALUES (:name, :email, :subscribe, :message)""" 

            my_data = {
                'name': name,
                'email': email,
                'subscribe': subscribe,
                'message': message
                }
         
            content = c.execute(query, my_data)
            conn.commit()

            print(f"Data Added ID: " + str(content.lastrowid))

        except sqlite3.Error as e:
            print(e)
       
        return redirect(url_for('thankyou'))
    
    return render_template('contact.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
