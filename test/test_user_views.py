"""User view tests."""

# run test: python3 -m unittest test_user_views.py

from unittest import TestCase
from models import db, User, Favorite

from app import app, session
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipe-test'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()
    
class UserViewTestCase(TestCase):
    """Test views."""
    
    def setUp(self):
      """Create test client, add sample data."""
      
      with app.app_context():
          db.drop_all()
          db.create_all()

          self.user = User.signup(
              username="johnSmith", 
              password="password", 
              email="johnsmith@test.com", 
              first_name="John", 
              last_name="Smith"
          )
          
          self.user_id = 8989
          self.user.id = self.user_id
          
          recipe = Favorite(
              recipe_id='716429',
              recipe_title='Pasta with Garlic',
              recipe_img="https://spoonacular.com/recipeImages/716429-556x370.jpg",
              user_id=self.user.id,
            )
        
          db.session.add(recipe)
          db.session.commit()
          
          self.username = self.user.username
          self.recipe_id = recipe.recipe_id
          
          self.client = app.test_client()
          
          with self.client.session_transaction() as sess:
              sess['username'] = self.username
          
          
          
    def tearDown(self):
        with app.app_context():
            res = super().tearDown()
            db.session.rollback()
            return res
            
    # def test_users_index(self):
    #     with self.client as c:
    #         resp = c.get(f"/users/{self.username}")
    #         html = resp.get_data(as_text=True)
            
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Search Recipe", html)
            
    # def test_users_favorites(self):
    #     with self.client as c:
    #         resp = c.get(f"/users/{self.username}/favorites")
    #         html = resp.get_data(as_text=True)
            
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Favorites", html)
            
    # def test_users_get_recipe(self):
    #     with self.client as c:
    #         url = f"/getRecipe/{self.recipe_id}"
    #         resp = c.get(url)
    #         html = resp.get_data(as_text=True)
            
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("Pasta with Garlic", html)    
    
    # def test_get_recipes(self):
    #     with self.client as c:
    #         url = "/recipes/burgers/1"
    #         resp = c.get(url)
    #         data = resp.json
    #         html = resp.get_data(as_text=True)
            
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertEqual(len(data), 10)
    #         self.assertIn("Loaded Turkey Burgers", html)
    #         self.assertNotIn("Pasta and Garlic", html)
            
    # def test_get_random_recipes(self):
    #     with self.client as c:
    #         url = "/random_recipes"
    #         resp = c.get(url)
    #         data = resp.json
            
    #         self.assertEqual(resp.status_code, 200)
    #         self.assertEqual(len(data), 10)
            
    
            