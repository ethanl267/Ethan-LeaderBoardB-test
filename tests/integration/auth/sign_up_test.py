
# from werkzeug.wrappers import request
# from website.auth import log_in
# from flask.wrappers import Response
from tests.base_test import BaseTest, db
from website.models import User
from flask_login import current_user
from flask import request

class TestSignUp(BaseTest):

    # test sign up user successfully 
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
    def test_log_in_success(self):
        with self.app:
            response = self.app.post('/sign-up',
                                    data=dict(email='moses@gmail.com', firstName="moses", password1='qwerty123', password2='qwerty123'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='moses@gmail.com').first()
            self.assertTrue(user)

            response = self.app.post('/log-in',
                                    data=dict(email='moses@gmail.com', password='qwerty123'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='moses@gmail.com').first()
            self.assertTrue(user)
            self.assertIn(b'Logged in successfully', response.data)

    def test_log_in_invalid_user(self):
        with self.app:
             response = self.app.post('/log-in',
                                    data=dict(email='qwers@gmail.com', password='qwerty123'),
                                    follow_redirects=True)
             self.assertIn(b'Email does not exist', response.data)

    def test_log_in_wrong_password(self):
        with self.app:
            response = self.app.post('/sign-up',
                                    data=dict(email='qwerss@gmail.com', firstName="moses", password1='qwerty123', password2='qwerty123'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='qwerss@gmail.com').first()
            self.assertTrue(user)


            response = self.app.post('/log-in',
                                    data=dict(email='qwerss@gmail.com', password='1234567'),
                                    follow_redirects=True)
                       
            self.assertIn(b'Password is wrong', response.data)



class TestLogout(BaseTest):
    def test_log_out(self):
        with self.app:
            Response =  response = self.app.post('/sign-up',
                                    data=dict(email='ethan@gmail.com', firstName="ethan", password1='qwers123', password2='qwers123'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='ethan@gmail.com').first()
            self.assertTrue(user)

            Response =  response = self.app.post('/log-in',
                                    data=dict(email='ethan@gmail.com', password='qwers123'),
                                    follow_redirects=True)
            user = db.session.query(User).filter_by(email='ethan@gmail.com').first()
            self.assertTrue(user)
            self.assertIn(b'Logged in successfully', response.data)

            response = response = self.app.get('/log-out', follow_redirects=True)
            self.assertEqual(response.status_code , 200)
            self.assertIn("/log-in", request.url)
            self.assertFalse(current_user.is_active)


