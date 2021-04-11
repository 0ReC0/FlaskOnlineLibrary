import base64
from encodings.base64_codec import base64_encode
from io import BytesIO
from os import abort

from flask import Blueprint, redirect, render_template, send_file
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.book_models import BookForm, Book

from base64 import b64encode

book_blueprint = Blueprint('book', __name__, template_folder='templates')


def allowed_file(filename, type="file"):
    al = {'fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'}
    if type == 'img':
        al = {'jpg', 'jpeg', 'png'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in al


@book_blueprint.route('/public_books', methods=['GET'])
def public_books():
    db_sess = db.session
    books = db_sess.query(Book).filter(Book.is_private != True).all()

    def append_img_src(book):
        img_base = base64.b64encode(book.image_data)
        img_base64 = img_base.decode('ascii')
        book.img_src = img_base64
        return book

    books = list(map(append_img_src, books))
    return render_template("book/public_books.html", books=books)


@book_blueprint.route('/book_download/<int:id>', methods=['GET'])
@login_required
def book_download(id):
    db_sess = db.session
    book = db_sess.query(Book).filter(Book.id == id).first()
    if book:
        return send_file(BytesIO(book.file_data), attachment_filename=book.file_name, as_attachment=True)
    else:
        abort(404)
    return redirect('/public_books')


@book_blueprint.route('/add_book', methods=['GET', 'POST'])
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
                                           f", разрешенные "
                                           f"({', '.join(['fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'])})",
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

# @book_blueprint.route('/book_edit/<int:id>', methods=['GET', 'POST']) @login_required def edit_book(id): form =
# BookForm() if request.method == "GET": db_sess = db.session book = db_sess.query(Book).filter(Book.id == id).first(
# ) if book: form.title.data = book.title form.is_private.data = book.is_private form.author.data = book.author,
# image_base64 = b64encode(book.image_data).decode("utf-8") else: abort(404) if form.validate_on_submit(): db_sess =
# db.session image = form.image.data file = form.file.data if not (image and allowed_file(image.filename,
# type='img')): return render_template('book/add_book.html', title='Добавление книги', message=f"Неверный формат
# картинки" f", разрешенные ({', '.join(['jpg', 'jpeg', 'png'])})", form=form) if not (file and allowed_file(
# file.filename)): return render_template('book/add_book.html', title='Добавление книги', message=f"Неверный формат
# файла" f", разрешенные ({', '.join(['fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'])})", form=form) book = Book(
# title=form.title.data, author=form.author.data, image_name=image.filename, image_data=image.read(),
# file_name=file.filename, file_data=file.read(), is_private=form.is_private.data ) db_sess.add(book) db_sess.commit(
# ) return redirect('/') if form.validate_on_submit(): db_sess = db.session book = db_sess.query(Book).filter(Book.id
# == id).first() if book: image = form.image.data file = form.file.data if not (image and allowed_file(
# image.filename, type='img')): return render_template('book/edit_book.html', title='Редактирование книги',
# message=f"Неверный формат картинки" f", разрешенные ({', '.join(['jpg', 'jpeg', 'png'])})", form=form) if not (file
# and allowed_file(file.filename)): return render_template('book/edit_book.html', title='Редактирование книги',
# message=f"Неверный формат файла" f", разрешенные ({', '.join(['fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'])})",
# form=form) book.title = form.title.data, book.author = form.author.data, book.image_name = image.filename,
# book.image_data = image.read(), book.file_name = file.filename, book.file_data = file.read(), book.is_private =
# form.is_private.data db_sess.commit() return redirect('/') else: abort(404) return render_template(
# 'book/edit_book.html', title='Редактирование книги', form=form )

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
