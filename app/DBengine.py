from app import db
from app.models import Author, Book, Hire
import datetime


class Data_guide_reader():

    def get_books_list(self, id=None):
        if bool(id):
            return Book.query.get(id)
        else:
            return Book.query.all()

    def get_author_list(self, id=None):
        if bool(id):
            return Author.query.get(id)
        else:
            return Author.query.all()

    def get_hire_list(self, book_id):
        if bool(id):
            book = self.get_books_list(book_id)
            return book.hire.all()
        else:
            return Hire.query.all()

    def create_author(self, author_name):
        author = Author(author_name=author_name)
        db.session.add(author)
        db.session.commit()

    def create_book(self, data, author=None):
        title = data.get("title")
        description = data.get("description")
        created = data.get("created")

        book = Book(title=title, description=description, created=created)
        db.session.add(book)
        db.session.commit()
        if author != None:
            author_name = data.get("author")
            author = Author.query.filter_by(author_name=author_name).first()
            if bool(author):
                book = Book.query.filter_by(title=title).first()
                author.books.append(book)
                db.session.commit()
            else:
                self.create_author(author_name)
                author = Author.query.filter_by(author_name=author_name).first()
                book = Book.query.filter_by(title=title).first()
                author.books.append(book)
                db.session.commit()

    def create_hire(self, data, book_id):
        borrower = data.get("name")
        date_hire = datetime.date.today()
        where = data.get("where")

        hire = Hire(borrower=borrower, date_hire=date_hire, where=where)

        db.session.add(hire)
        db.session.commit()
        hire_id = hire.id

        book = Book.query.get(book_id)
        hire = Hire.query.get(hire_id)
        book.hire.append(hire)
        db.session.commit()

    def delete_author(self, author_id):
        author = Author.query.get(author_id)
        db.session.delete(author)
        db.session.commit()

    def delete_hire(self, book_id):
        book = Book.query.get(book_id)
        for i in book.hire.all():
            db.session.delete(i)
        db.session.commit()

    def delete_book(self, book_id):
        book = Book.query.get(book_id)
        hire = book.hire.all()
        db.session.delete(book)
        db.session.commit()

        for i in hire:
            db.session.delete(i)
        db.session.commit()

    def edit_book(self, book_id, data):
        if not data.get("title") == None:
            book = Book.query.get(book_id)

            book.title = data.get("title")
            book.description = data.get("description")
            book.created = data.get("created")

            db.session.add(book)
            db.session.commit()

    def get_data_to_book_form(self,book_id):
        book = Book.query.get(book_id)
        data = {"title":book.title,"description":book.description,"created":book.created}
        return data

    def add_author(self,book_id,data):
        print("add_author")
        author_name = data.get("author")
        author = Author.query.filter_by(author_name=author_name).first()
        book = Book.query.get(book_id)

        if bool(author):
            print(True)
            author.books.append(book)
            db.session.commit()

        else:
            print(False)
            self.create_author(author_name)
            author = Author.query.filter_by(author_name=author_name).first()

            author.books.append(book)
            db.session.commit()




guide = Data_guide_reader()
