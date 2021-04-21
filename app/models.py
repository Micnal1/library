from datetime import datetime
from app import db
from sqlite3 import connect

books = db.Table('books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), index=True, unique=True)
    books = db.relationship("Book",secondary=books ,backref=db.backref('authors', lazy="dynamic"))

    def __str__(self):
        return f"<User {self.author_name}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    created = db.Column(db.Integer, index=True, default=datetime.utcnow)
    hire = db.relationship("Hire", backref="book", lazy="dynamic")

    def __str__(self):
        return f"<Post {self.id} {self.body[:50]} ...>"


class Hire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower = db.Column(db.Text)
    date_hire = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    where = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __str__(self):
        return f"<Post {self.id} {self.borrower[:50]} ...>"


class Data_Reader_Author():
    author_list = []
    book_list = []
    hire_list = []

    def get_data(self, data_type):
        connection = connect("library.db")
        cur = connection.cursor()
        cur.execute(f"SELECT * FROM {data_type};")
        return cur.fetchall()

    def get_id(self, id):
        id_list = list(map(int, id.split(",")))
        return id_list

    def get_author(self):
        self.author_list = self.get_data("author")
        self.author_list = [{"id": id, "author_name": name} for id, name in self.author_list]
        return self.author_list

    def get_book(self):
        self.book_list = self.get_data("book")
        self.book_list = \
            [{"id": id,
              "title": title,
              "description": description,
              "created": created,
              "author_id": self.get_id(author_id)} for id, title, description, created, author_id in self.book_list]
        return self.book_list

    def get_hire(self):
        self.hire_list = self.get_data("hire")
        if bool(self.hire_list):

            self.hire_list = \
                [{"id": id,
                  "borrower": borrower,
                  "date_hire": date_hire,
                  "where": where,
                  "book_id": int(book_id)} for id, borrower, date_hire,where, book_id in self.hire_list]
            return self.hire_list
        else:
            return []


data_guide = Data_Reader_Author()


class Hire_Writer(Data_Reader_Author):

    def give_hire(self, data, book_id):
        hire_data = self.get_data("hire")
        if bool(hire_data):
            id = max([i[0] for i in hire_data]) + 1

        else:
            id = 1
        book_id = str(book_id)
        borrower = data.get("name")
        date_hire = str(data.get("date_hire"))
        where = str(data.get("where"))

        connection = connect("library.db")
        cur = connection.cursor()
        cur.execute(f'INSERT INTO hire VALUES ({id},"{borrower}","{date_hire}","{where}",{book_id});')
        connection.commit()


writer = Hire_Writer()

