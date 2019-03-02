from flask import Flask, request, json, Response, redirect, url_for, render_template, flash
import pymongo
import os
import datetime

# start Flask app
app = Flask(__name__)
app.secret_key = 'geniosity'

# connect to online MongoDB Atlas database
mongo = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0-qhvlf.mongodb.net/test?retryWrites=true', maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo, 'FBLA')
student = pymongo.collection.Collection(db, 'Users')
book = pymongo.collection.Collection(db, 'Books')
history = pymongo.collection.Collection(db, 'History')

# home page
@app.route('/')
def index():
    return render_template('index.html', book=book.count(), student=student.count())

# checking out + tracking history
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    
    # if form is accessed
    if request.method == 'POST':

        print(request.form)

        # access the form data
        book, student = int(request.form.get('id')), int(request.form.get('student'))

        # make the document for MongoDB and insert
        profile = {
            'book': book,
            'student': student,
            'checkedout': datetime.datetime.utcnow()
        }
        history.insert_one(profile)

        # confirmation message
        flash(f'{book} checked out by {student} successfully.')
    
    # render
    return render_template('checkout.html', entries=history.find(
        {'checkedout': {
            '$gte': datetime.datetime.utcnow() - datetime.timedelta(days=7),
            '$lt': datetime.datetime.utcnow()
        }}
    ))

# interface for managing students
@app.route('/students', methods=['GET', 'POST'])
def students():

    # if form is accessed
    if request.method == 'POST':

        # access the form data
        name, grade = request.form.get('name'), int(request.form.get('grade'))

        # make the document for MongoDB and insert
        profile = {
            'name': name,
            'grade': grade,
            'added': datetime.datetime.utcnow()
        }
        student.insert_one(profile)

        # confirmation message
        flash(f'{name} in grade {grade} successfully added to database.')
    
    # render
    return render_template('students.html', entries=student.find({}))
    

@app.route('/books')
def books():
    
    # if form is accessed
    if request.method == 'POST':

        # make the document for MongoDB and insert
        profile = {
            'title': request.form.get('title'),
            'isbn': request.form.get('isbn'),
            'code': request.form.get('code'),
            'checkedout': request.form.get('checkedout'),
            'last': datetime.datetime.utcnow()
        }
        book.insert_one(profile)

        # confirmation message
        flash(f'{title} (code {code}) successfully added to database.')
    
    # render
    return render_template('books.html', entries=book.find({}))