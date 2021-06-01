from app import app, db
from app.models import User, Autobase
import unittest

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()
    
    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
    
    def test_password_hashing(self):
        u = User(username='cat')
        u.set_password('dog')
        self.assertFalse(u.check_password('tiger'))
        self.assertTrue(u.check_password('dog'))

if __name__ == '__main__':
    unittest.main(verbosity=2)