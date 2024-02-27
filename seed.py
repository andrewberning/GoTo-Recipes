from app import app
from models import db, User, Favorite

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User.signup(
      username="testUser1",
      password="testUser1PW",
      email="testUser1@test.com",
      first_name="test",
      last_name="User"
    )
    
    favRecipe1 = Favorite(
      recipe_id='716429',
      recipe_title='Pasta with Garlic',
      recipe_img="https://spoonacular.com/recipeImages/716429-556x370.jpg",
      user_id='1',
    )
    
    favRecipe2 = Favorite(
      recipe_id='716435',
      recipe_title='Herbed Goat Cheese Yogurt Dip w. Caramelized Onions',
      recipe_img="https://spoonacular.com/recipeImages/716435-556x370.jpg",
      user_id='1',
    )
    
    db.session.add_all([user1, favRecipe1, favRecipe2])

    db.session.commit()