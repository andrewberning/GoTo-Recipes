"""User Model Tests."""

# run test: python3 -m unittest ./tests/test_user_model.py


from flask import session
from unittest import TestCase
from models import db, User, Favorite
from sqlalchemy import exc


from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipe-test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True
app.testing = True

with app.app_context():
    db.drop_all()
    db.create_all()

class UserModelTestCase(TestCase):
    """Test views """

    def setUp(self):
        """Add sample user."""
        with app.app_context():
            db.drop_all()
            db.create_all()
            
            user = User.signup(
              "johnSmith", "password", "johnsmith@test.com", "John", "Smith"
            )
            db.session.commit()
            
            user1 = db.session.query(User).get(user.id)
            self.user1 = user1

          
            self.client = app.test_client()
            
    def tearDown(self):
        with app.app_context():
            res = super().tearDown()
            db.session.rollback()
            return res

      
    def test_user_model(self):
        """Test user model."""
        
        with app.app_context():
            user = User(
                username="testuser", 
                password="hashed_password", 
                email="testuser@test.com", 
                first_name="test", 
                last_name="user"
            )
            
            db.session.add(user)
            db.session.commit()
            
            self.assertEqual(user.username, "testuser")
            self.assertEqual(user.email, "testuser@test.com")
            self.assertEqual(user.first_name, "test")
            self.assertEqual(user.last_name, "user")
            self.assertEqual(len(user.favorites), 0)
        
    ##############################
    #        Signup Tests        #
    ##############################
    
    def test_valid_signup(self):
        """Test valid signup."""
      
        with app.app_context():
            valid_user = User.signup(
              "janeSmith", "janesmith", "janesmith@test.com", "Jane", "Smith"
            )
            uid = 999
            valid_user.id = uid
            db.session.commit()
        
            valid_user = db.session.query(User).get(valid_user.id)
            self.assertIsNotNone(valid_user)
            self.assertEqual(valid_user.id, 999)
            self.assertEqual(valid_user.username, "janeSmith")
            self.assertEqual(valid_user.email, "janesmith@test.com")
            self.assertEqual(valid_user.first_name, "Jane")
            self.assertEqual(valid_user.last_name, "Smith")
            self.assertEqual(len(valid_user.favorites), 0)
            
            
    def test_invalid_username_signup(self):
        """Test invalid username signup."""
        
        with app.app_context():
            invalid_user = User.signup(
              None, "password", "pauljones@test.com", "Paul", "Jones"
            )
            uid = 777
            invalid_user.id = uid
            
            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()
                
    def test_invalid_email_signup(self):
        """Test invalid email signup."""
        
        with app.app_context():
            invalid_user = User.signup(
              "tester1", "password", None, "Shirly", "Thomas"
            )
            uid = 5555
            invalid_user.id = uid
            
            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit() 
                
    def test_invalid_password_signup(self):
        """Test invalid password signup."""
        
        with app.app_context():
            with self.assertRaises(ValueError) as context:
                User.signup(
                  "tester2", None, "tester2@test.com", "Gordy", "Holms"
                )
            
            with self.assertRaises(ValueError) as context:
                User.signup(
                  "tester2", "", "tester2@test.com", "Gordy", "Holms"
                )
                
    
    ##############################
    #     Authentication Tests   #
    ##############################
    
    def test_valid_authentication(self):
        with app.app_context():
            u = User.authenticate(self.user1.username, "password")
            
            self.assertIsNotNone(u)
            self.assertEqual(u.id, self.user1.id)
            
    def test_invalid_username(self):
        with app.app_context():
            self.assertFalse(User.authenticate("badusername", "password"))
            
    def test_invalid_password(self):
        with app.app_context():
            self.assertFalse(User.authenticate(self.user1.username, "badpassword"))
            
    