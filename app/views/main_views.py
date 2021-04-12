import secrets

from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm, GetApiForm, User

main_blueprint = Blueprint('main', __name__, template_folder='templates')


# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)


@main_blueprint.route('/main/get_api_key', methods=['GET', 'POST'])
@login_required
def get_api_key():
    # Initialize form
    form = GetApiForm()

    if request.method == 'POST':
        db_sess = db.session
        user = db_sess.query(User).filter_by(id=current_user.id).first()
        user.api_key = secrets.token_urlsafe(20)
        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.get_api_key'))

    # Process GET or invalid POST
    return render_template('main/get_api_key.html',
                           form=form)


@main_blueprint.app_errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@main_blueprint.app_errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


@main_blueprint.app_errorhandler(Exception)
def unhandled_exception(error):
    return render_template("errors/500.html"), 500
