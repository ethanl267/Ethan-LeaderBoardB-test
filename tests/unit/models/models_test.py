from unittest import TestCase
from website.models import Note, Work, User, Team

class TestAllModels(TestCase):

    def test_note_is_created(self):
        new_note = Note(data='new note!')
        # checking if our note class is functional
        self.assertEqual(new_note.data, 'new note!') 

    def test_work_is_created(self):
        new_work = Work(title='New Work', 
                        description='you need to do this task',
                        user_id=2,
                        status='to-do',
                        points=300)
        # checking if our work class is functional
        self.assertEqual(new_work.title, 'New Work')
        self.assertEqual(new_work.description, 'you need to do this task')
        self.assertEqual(new_work.user_id, 2)
        self.assertEqual(new_work.status, 'to-do')
        self.assertEqual(new_work.points, 300)

    def test_user_is_created(self):
        new_user = User(email='mail@gmail.com', 
                        password='pass1234', 
                        first_name='Namey',
                        team_id= 0,
                        team_leader= False,
                        points= 0)
        self.assertEqual(new_user.email, 'mail@gmail.com')
        self.assertEqual(new_user.password, 'pass1234')
        self.assertEqual(new_user.first_name, 'Namey')
        self.assertEqual(new_user.team_id, 0)
        self.assertEqual(new_user.team_leader, False)
        self.assertEqual(new_user.points, 0)

    def test_team_is_created(self):
        new_team = Team(name='TeamZee')
        self.assertEqual(new_team.name, 'TeamZee')