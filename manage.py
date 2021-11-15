from app import create_app,db
from flask_script import Manager
from flask_script import Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User

# Creating app instance
app = create_app('production') #Update for production

manager = Manager(app)
manager.add_command('server',Server)
# Create flask schema
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User)


if __name__ == '__main__':
    manager.run()
