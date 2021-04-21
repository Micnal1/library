from app import forms
from flask import render_template, request, redirect, url_for

from biblioteka import *
from app.DBengine import guide


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    form = forms.Book_and_author()
    data = request.form
    if request.method == 'POST':
        guide.create_book(data, 1)
        return redirect(url_for("add_book"))

    return render_template("add_author.html", form=form)


@app.route("/", methods=["GET", "POST"])
def homepage():
    selected_list = request.args.get("current_list", "1")
    books = Book.query.all()
    authors = Author.query.all()

    form = forms.Book_and_author()
    data = request.form
    if request.method == 'POST':
        guide.create_book(data, 1)
        return redirect(url_for("homepage"))

    return render_template("homepage.html", books=books, authors=authors, selected_list=selected_list, form=form)


@app.route("/books/<int:book_id>/details", methods=["GET", "POST"])
def books_details_page(book_id):
    book = Book.query.get(book_id)

    form = forms.Hire()
    form2 = forms.Book(data=guide.get_data_to_book_form(book_id))
    data = request.form

    if request.method == 'POST' and form.validate():
        print("fuck!")
        guide.create_hire(data, book_id)
        return redirect(url_for("books_details_page", book_id=book_id))

    if request.method == 'POST' and form2.validate and data.get("author") == None:
        print("fuck")
        guide.edit_book(book_id, data)
        return redirect(url_for("books_details_page", book_id=book_id))

    return render_template("books_details.html", book=book, form=form, form2=form2, book_id=book_id)


@app.route("/author/<int:author_id>/details", methods=["GET", "POST"])
def authors_details_page(author_id):
    author = Author.query.get(author_id)
    form = forms.Edit_author(data={"author": author.author_name})
    data = request.form
    data = data.get("author")
    if request.method == 'POST' and form.validate():
        author.author_name = data
        db.session.add(author)
        db.session.commit()

    return render_template("author_details.html", author=author, form=form)


@app.route("/author/<int:author_id>/delete")
def delete_author(author_id):
    guide.delete_author(author_id)
    return redirect(url_for("homepage"))


@app.route("/book/<int:book_id>/delete")
def delete_book(book_id):
    guide.delete_book(book_id)
    return redirect(url_for("homepage"))


@app.route("/book/<int:book_id>/hire/delete")
def delete_hire(book_id):
    guide.delete_hire(book_id)
    return redirect(url_for("books_details_page", book_id=book_id))


@app.route("/book/<int:book_id>/add_author", methods=["GET", "POST"])
def add_authors(book_id):
    form = forms.Edit_author()
    data = request.form
    if request.method == 'POST' and form.validate():
        print("jest")
        guide.add_author(book_id, data)
        return redirect(url_for("books_details_page", book_id=book_id))
    return render_template("add_author.html", form=form, book_id=book_id)
