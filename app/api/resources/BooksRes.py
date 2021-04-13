from flask import jsonify
from flask_restful import Resource, reqparse

from app.models.book_models import Book
from app.models.user_models import User

parser = reqparse.RequestParser()
parser.add_argument('api_key', type=str)


class BooksRes(Resource):
    def get(self):
        args = parser.parse_args()
        api_key = args['api_key']
        if api_key:
            user_api = User.query.filter(User.api_key == api_key).first()
            if user_api:
                books = Book.query.order_by(Book.title).all()
                return jsonify(Book.serialize_list(books))
        books = Book.query.filter(Book.is_private == False).order_by(Book.id).all()
        return jsonify(Book.serialize_list(books))
