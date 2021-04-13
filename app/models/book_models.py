import base64

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired

from app import db
from app.api.resources.Serializer import Serializer


class Book(db.Model, Serializer):
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

    def serialize(self):
        ser_temp = Serializer.serialize(self)
        img_base = base64.b64encode(ser_temp['image_data'])
        img_base64 = img_base.decode('ascii')
        ser_temp['image_data'] = img_base64
        del ser_temp['file_data']
        return ser_temp


class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    image = FileField("Картинка", validators=[FileRequired()])
    file = FileField("Файл книги", validators=[FileRequired()])
    is_private = BooleanField("Сделать книгу приватной, т.е. доступной только для зарегистрированных пользователей")
    submit = SubmitField('Добавить')


class BookEditForm(BookForm):
    image = FileField("Картинка", validators=[])
    file = FileField("Файл книги", validators=[])