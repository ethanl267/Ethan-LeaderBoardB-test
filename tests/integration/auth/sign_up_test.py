from website.auth import log_in
from flask.wrappers import Response
from tests.base_test import BaseTest, db
from website.models import User
from flask_login import current_user

class TestSignUp(BaseTest):

    # test signing up user successfully 
    def test_sign_up_post_success(self):
        with self.app:
            # create a post req with valid data
            response = self.app.post('/sign-up',
                                    data=dict(email='email@gmail.com', firstName='Namey', password1='pass1234', password2='pass1234'),
                                    follow_redirects=True)
            # assert that new user is created in db
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)
            # assert that flash message is shown
            self.assertIn(b'Account created', response.data)
            # assert that user is logged in 
            self.assertEqual(current_user.get_id(), '1')
            # assert that page is redirected
            self.assertIn(b'Notes', response.data)

    def test_sign_up_post_user_exists(self):
        with self.app:
            response = self.app.post('/sign-up',
                                    data=dict(email='email@gmail.com', firstName='Namey', password1='pass1234', password2='pass1234'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)

            response = self.app.post('/sign-up',
                                    data=dict(email='email@gmail.com', firstName='Namey', password1='pass1234', password2='pass1234'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)

            self.assertIn(b'Email already in use',response.data)

class Testlog_in(BaseTest):
    def test_log_in_post(self):
        with self.app:
            response = self.app.post('/log-in',
                                    data=dict(email='email@gmail.com', password1='pass1234'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            user_data = self.app.post('/log-in', email='email@gmail.com', password='pass1234')
            self.assertIn(b'Logged in successfully', user_data.data)