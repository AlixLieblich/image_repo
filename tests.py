from unittest import TestCase
from server import app
import crud 
from model import User, Image, connect_to_db, db, example_data
import os 

# def test_data():
#     """Make test data for teting."""

#     #create user with: username, password, first name, last name, email
#     user = crud.create_user('photographer24', 'test', 'Smokey', 'Bear', 'hiker@gmail.com')
#     #create image with user id, image name, and three tags
#     image=crud.create_image(1, '', 'Denali', 'Nature', 'Pretty')

class FlaskTestCase(TestCase):
    def setUp(self):
        """Routine before test starts."""

        #Get Flask test client
        self.client = app.test_client
        #Show errors from Flask than happen
        app.config['TESTING'] = True
        #Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        #Create tables and add sample data to them
        db.create_all()
        example_data()

    def tearDown(self):
        """To be done at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_user(self):
        """Test for user in test data."""

        user = User.query.filter(User.user_fname == "Smokey").first()
        self.assertEqual(user.user_fname, "Smokey")

    def test_image(self):
        """Test for image in test data."""

        image = Image.query.filter(Image.tag1 == "Denali").first()
        self.assertEqual(image.tag1, "Denali")

if __name__ == '__main__':
    import unittest

    os.system('dropdb testdb')
    os.system('createdb testdb')

    unittest.main(verbosity=2)   