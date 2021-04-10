import os

# *****************************
# Environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
from flask import logging

DEBUG = True

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#     python -c "import os; print(repr(os.urandom(24)));"
SECRET_KEY = '\x92UIW\xa5U\n$\x82\xaa\xcb\xf5\xab\xa2\x0e\xc7\xab\xf9\x86\xa67\xae\xbc\xe4'

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../app.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids a SQLAlchemy Warning

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps" to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps (near the bottom).
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = 'temp74054@gmail.com'
MAIL_PASSWORD = 'temp74054Temp'
MAIL_DEFAULT_SENDER = 'temp74054@gmail.com'

# Flask-User settings
USER_APP_NAME = 'Flask-Online-Library'
USER_EMAIL_SENDER_NAME = 'temp74054'
USER_EMAIL_SENDER_EMAIL = 'temp74054@gmail.com'

# Setting for file upload, max 30 MB
UPLOAD_FOLDER = 'D:/uploads'
MAX_CONTENT_LENGTH = 30 * 1024 * 1024

ADMINS = [
    '"Admin One" <temp74054@gmail.com>',
    ]
