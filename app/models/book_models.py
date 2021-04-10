from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, validators, TextAreaField, BooleanField, FileField
from wtforms.validators import DataRequired

from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    image_name = db.Column(db.String(300))
    image_data = db.Column(db.LargeBinary)
    file_name = db.Column(db.String(300))
    file_data = db.Column(db.LargeBinary)
    author = db.Column(db.String(80))
    is_private = db.Column(db.Boolean, unique=False, default=True)

    def __init__(self, title, author, image_name, image_data, file_name, file_data, is_private):
        self.title = title
        self.author = author
        self.image_name = image_name
        self.image_data = image_data
        self.file_name = file_name
        self.file_data = file_data
        self.is_private = is_private

    def __repr__(self):
        return "<Book %r>" % self.title


class BookForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    image = FileField("Картинка", validators=[FileRequired()])
    file = FileField("Файл книги", validators=[FileRequired()])
    is_private = BooleanField("Для зарегистрированных пользователей")
    submit = SubmitField('Добавить')