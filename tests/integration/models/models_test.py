from tests.base_test import BaseTest, db
from website.models import Note


# class that tests if models can be saved and deleted from dbs
class TestModelsCrud(BaseTest):
    

    # test that notes can be saved and deleted from db
    def test_note_crud(self):
        # calling app context
        with self.app_context:
            # create new note
            new_note = Note(data='New memo or stuff')
        
            # assert that this item does not exist in the db
            results = db.session.query(Note).filter_by(data='New memo or stuff').first()
            self.assertIsNone(results)

            # save to db
            db.session.add(new_note)
            db.session.commit()

            # assert that it does exist in db
            results = db.session.query(Note).filter_by(data='New memo or stuff').first()
            self.assertIsNotNone(results)

            # delete from db
            db.session.delete(new_note)
            db.session.commit()

            # assert it no longer exists in db
            results = db.session.query(Note).filter_by(data='New memo or stuff').first()
            self.assertIsNone(results)