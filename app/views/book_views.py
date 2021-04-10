from os import abort

from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.book_models import BookForm, Book

book_blueprint = Blueprint('book', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = {'fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'}
ALLOWED_EXTENSIONS_IMG = {'jpg', 'jpeg', 'png'}


def allowed_file(filename, type="file"):
    al = {'fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'}
    if type == 'img':
        al = {'jpg', 'jpeg', 'png'}

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in al


@book_blueprint.route('/book_add',  methods=['GET', 'POST'])
@roles_required('admin')
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        db_sess = db.session
        image = form.image.data
        file = form.file.data
        if not (image and allowed_file(image.filename, type='img')):
            return render_template('book/add_book.html', title='Добавление книги',
                                   message=f"Неверный формат картинки"
                                           f", разрешенные ({', '.join(['jpg', 'jpeg', 'png'])})",
                                   form=form)
        if not (file and allowed_file(file.filename)):
            return render_template('book/add_book.html', title='Добавление книги',
                                   message=f"Неверный формат файла"
                                           f", разрешенные ({', '.join(['fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'])})",
                                   form=form)
        book = Book(title=form.title.data,
                    author=form.author.data,
                    image_name=image.filename,
                    image_data=image.read(),
                    file_name=file.filename,
                    file_data=file.read(),
                    is_private=form.is_private.data
                    )
        db_sess.add(book)
        db_sess.commit()
        return redirect('/')
    return render_template('book/add_book.html', title='Добавление книги',
                           form=form)

# @book_blueprint.route('/book/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_book(id):
#     form = NewsForm()
#     if request.method == "GET":
#         db_sess = db.create_session()
#         book = db_sess.query(News).filter(News.id == id,
#                                           News.user == current_user
#                                           ).first()
#         if book:
#             form.title.data = book.title
#             form.content.data = book.content
#             form.is_private.data = book.is_private
#         else:
#             abort(404)
#     if form.validate_on_submit():
#         db_sess = db.create_session()
#         book = db_sess.query(News).filter(News.id == id,
#                                           News.user == current_user
#                                           ).first()
#         if book:
#             book.title = form.title.data
#             book.content = form.content.data
#             book.is_private = form.is_private.data
#             db_sess.commit()
#             return redirect('/')
#         else:
#             abort(404)
#     return render_template('book.html',
#                            title='Редактирование новости',
#                            form=form
#                            )
#
# @book_blueprint.route('/book_delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def book_delete(id):
#     db_sess = db.create_session()
#     book = db_sess.query(News).filter(News.id == id,
#                                       News.user == current_user
#                                       ).first()
#     if book:
#         db_sess.delete(book)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')
