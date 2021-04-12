from flask import jsonify
from flask_restful import Resource, abort, reqparse

from app.models.book_models import Book
from app.models.user_models import User

parser = reqparse.RequestParser()
parser.add_argument('api_key', type=str)


class BookRes(Resource):
    def get(self, id):
        args = parser.parse_args()
        api_key = args['api_key']
        if api_key:
            user_api = User.query.filter(User.api_key == api_key).first()
            if user_api:
                book = Book.query.filter(Book.id == id).first()
                if not book:
                    abort(404, description="Book not found")
                return jsonify(Book.serialize(book))
        book = Book.query.filter(Book.is_private == False).filter(Book.id == id).first()
        if not book:
            abort(404, description="Book not found")
        return jsonify(Book.serialize(book))