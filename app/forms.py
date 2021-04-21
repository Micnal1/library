from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class Hire(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    where = SelectField('where', choices=[("wypożyczenie", "wypożyczone"), ("oddanie", "na półce")],
                        validators=[DataRequired()])


class Book(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    created = StringField('created', validators=[DataRequired()])


class Book_and_author(Book):
    author = StringField('author', validators=[DataRequired()])


class Edit_author(FlaskForm):
    author = StringField('author', validators=[DataRequired()])
