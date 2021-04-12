"""This file sets up a command line manager.

Use "python main.py" for a list of available commands.
Use "python main.py runserver" to start the development web server on localhost:5000.
Use "python main.py runserver --help" for a list of runserver options.
"""
import os

from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app
from app.commands import InitDbCommand

app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('init_db', InitDbCommand)

if __name__ == "__main__":
    # python main.py                      # shows available commands
    # python main.py runserver --help     # shows available runserver options
    # manager.run({'init_db': InitDbCommand()})
    # port = int(os.environ.get("PORT", 5000))
    # manager.app.run(host='0.0.0.0', port=port)
    manager.run()