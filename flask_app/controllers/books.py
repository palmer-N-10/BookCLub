from flask import render_template, request, redirect, session,flash
from flask_app import app
from flask_app.models.book import book

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/book/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_book.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/book/create',methods=['POST'])
def create():
    print(request.form)
    if not book.validate_book(request.form):
        return redirect('/book/new')
    id = book.save(request.form)
    print(id)
    return redirect('/books')


# TODO READ ALL
@app.route('/books')
def books():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("books.html",books=book.get_all())

# # TODO READ ONE
@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id": id
    }
    x=book.get_one(data)
    return render_template("show.html",book=x)


# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/book/update',methods=['POST'])
def update():
    book.update(request.form)
    return redirect('/books')

# ! ///// DELETE //////
@app.route('/book/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    book.destroy(data)
    return redirect('/books')