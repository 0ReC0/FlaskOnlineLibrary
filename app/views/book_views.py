import base64
from io import BytesIO
from os import abort

from flask import Blueprint, redirect, render_template, send_file, request
from flask_user import login_required, roles_required

from app import db
from app.models.book_models import BookForm, Book, BookEditForm

book_blueprint = Blueprint('book', __name__, template_folder='templates')


@book_blueprint.route('/public_books', methods=['GET'])
def public_books():
    db_sess = db.session
    books = db_sess.query(Book).filter(Book.is_private != True).all()
    books = list(map(append_img_src, books))
    return render_template("book/public_books.html", books=books)


@book_blueprint.route('/private_books', methods=['GET'])
@login_required
def private_books():
    db_sess = db.session
    books = db_sess.query(Book).filter(Book.is_private == True).all()
    books = list(map(append_img_src, books))
    return render_template("book/private_books.html", books=books)


@book_blueprint.route('/manage_books', methods=['GET'])
@roles_required('admin')
def manage_books():
    db_sess = db.session
    books = db_sess.query(Book).all()
    books = list(map(append_img_src, books))
    return render_template("book/manage_books.html", books=books)


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


@book_blueprint.route('/edit_book/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_book(id):
    form = BookEditForm()
    if request.method == "GET":
        db_sess = db.session
        book = db_sess.query(Book).filter(Book.id == id).first()
        if book:
            form.title.data = book.title
            form.author.data = book.author
            form.is_private.data = book.is_private
            form.image_name = book.image_name
            img_base = base64.b64encode(book.image_data)
            img_base64 = img_base.decode('ascii')
            form.image_data = img_base64
            form.file_name = book.file_name
            form.id = book.id
            return render_template('book/edit_book.html', title='Редактирование книги',
                                   form=form)
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db.session
        book = db_sess.query(Book).filter(Book.id == id).first()

        image = form.image.data
        file = form.file.data
        if image:
            if not allowed_file(image.filename, type='img'):
                return render_template('book/edit_book.html', title='Добавление книги',
                                       message=f"Неверный формат картинки"
                                               f", разрешенные ({', '.join(['jpg', 'jpeg', 'png'])})",
                                       form=form)
        if file:
            if not allowed_file(file.filename):
                return render_template('book/edit_book.html', title='Добавление книги',
                                       message=f"Неверный формат файла"
                                               f", разрешенные "
                                               f"({', '.join(['fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'])})",
                                       form=form)
        if book:
            if book.title != form.title.data:
                book.title = form.title.data
            if book.author != form.author.data:
                book.author = form.author.data
            if book.is_private != form.is_private.data:
                book.is_private = form.is_private.data
            if book.title != form.title.data:
                book.title = form.title.data
            if book.title != form.title.data:
                book.title = form.title.data
            if image:
                book.image_name = image.filename
                book.image_data = image.read()
            if file:
                book.file_name = file.filename
                book.file_data = file.read()
            db_sess.commit()
            return redirect('/manage_books')
        else:
            abort(404)
    return render_template('book/edit_book.html', title='Редактирование книги',
                           form=form)


@book_blueprint.route('/delete_book/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def delete_book(id):
    db_sess = db.session
    book = db_sess.query(Book).filter(Book.id == id).first()
    if book:
        db_sess.delete(book)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/manage_books')


def allowed_file(filename, type="file"):
    al = {'fb2', 'pdf', 'epub', 'aep', 'mobi', 'azw3'}
    if type == 'img':
        al = {'jpg', 'jpeg', 'png'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in al


def append_img_src(book):
    img_base = base64.b64encode(book.image_data)
    img_base64 = img_base.decode('ascii')
    book.img_src = img_base64
    return book
