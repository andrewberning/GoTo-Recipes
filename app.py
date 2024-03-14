from flask import Flask, flash, render_template, redirect, request, session, jsonify, g
import requests
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from models import db, connect_db, User, Favorite
from forms import RegisterForm, LoginForm
from keys import API_KEY
from utils import user_not_in_session, not_same_username, check_api

API_BASE_URL = "https://api.spoonacular.com/recipes"

######## CONFIG ########
app = Flask(__name__)

app.testing = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://svsnjiht:chOvowmwjkX084LmaBEtPQWCHNHHtoAV@bubble.db.elephantsql.com/svsnjiht'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"

connect_db(app)

with app.app_context():
    db.create_all()


@app.before_request
def add_user_to_g():
    """If we are logged in, add current user to Flask global."""
    
    if "username" in session:
        g.user = User.query.filter_by(username=session['username']).first()
    else:
        g.user = None

######## ROUTES ########

@app.route("/")
def index():
    "Redirect to login page."
    if g.user:
        return redirect(f"/users/{session['username']}")
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Show login page"""
      
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                form.password.data)
        
        if user:
            session['username'] = user.username
            flash(f"Welcome back {user.username}!", "success")
            return redirect(f"/users/{user.username}")
        else:
            flash("Invalid credentials. Try Again.", "danger")
            return render_template("users/login.html", form=form)
      
    return render_template("users/login.html", form=form)
  
@app.route("/logout")
def logout():
    """Logout user: 
        - remove user from session
        - redirect to login page.
    """
    session.pop("username")
    flash("Successfully logged out.", "success")
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    
  form = RegisterForm()
  
  if form.validate_on_submit():
    try:
        user = User.signup(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
        )
        
        db.session.commit()
        session["username"] = user.username
        
    except IntegrityError:
        flash("Username already exists. Try another.", "danger")
        return render_template("users/register.html", form=form)
      
    flash(f"Welcome {user.username}!", "success")  
    return redirect(f"/users/{user.username}")

  return render_template('/users/register.html', form=form)

######## USERS ROUTES #########

@app.route("/users/<username>")
def search(username):
    """Show user home page."""
    
    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(username):
        return redirect(f"/users/{session['username']}")
    
    return render_template("users/search.html", user=g.user)

@app.route("/users/<username>/favorites")
def favorites(username):
    """Show user favorite recipes."""

    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(username):
        return redirect(f"/users/{session['username']}")
    
    return render_template("users/favorites.html", user=g.user)
    
  
@app.route("/users/favorites/<int:id>", methods=["DELETE"])
def deleteFavoriteRecipe(id):
    """Delete recipe from database."""
    
    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(g.user.username):
        return redirect(f"/users/{session['username']}")
  
    favRecipe = Favorite.query.get_or_404(id)
    
    db.session.delete(favRecipe)
    db.session.commit()
    
    return jsonify(messag="Deleted")
  
@app.route("/users/favorites/add", methods=["POST"])
def add_to_favorites():
    """Add a recipe to your favorites list."""
    
    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(g.user.username):
        return redirect(f"/users/{session['username']}")
    
    data = request.json
    
    existing_favorite = Favorite.query.filter_by(
        recipe_id=data['recipeId'],
        user_id=g.user.id
    ).first()
    
    if existing_favorite:
        return jsonify({'success': False, 'message': 'Recipe already in favorites.'})

    new_fav = Favorite(
        recipe_id=data['recipeId'],
        recipe_title=data['recipeTitle'],
        recipe_img=data['recipeImage'],
        user_id=g.user.id,
    )
    
    db.session.add(new_fav)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Recipe added to favorites.'})

  
@app.route("/recipes/<query>/<page>")
def get_recipes(query, page):
    """Get recipes."""
    
    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(g.user.username):
        return redirect(f"/users/{session['username']}")
    
    check_api(API_KEY)
    url = f"{API_BASE_URL}/complexSearch"
    offsetStr = int(page) * 10

    queryParameters = {
      'apiKey': API_KEY,
      'query': query,
      'number': "10",
      'offset': str(offsetStr)
    }
    
    try:
        response = requests.get(url, params=queryParameters)
        response.raise_for_status()
        
        data = response.json()
        recipes = data["results"]
        
        return jsonify(recipes)
      
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch recipes: {e}")
  
@app.route("/random_recipes")
def get_random_recipes():
    """Get random recipes"""
    
    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(g.user.username):
        return redirect(f"/users/{session['username']}")
    
    check_api(API_KEY)  
    url = f"{API_BASE_URL}/random"
    
    queryParameters = {
      'apiKey': API_KEY,
      'number': "10"
    }
    
    try:
        response = requests.get(url, params=queryParameters)
        response.raise_for_status()
        
        data = response.json()
        recipes = data["recipes"]
        
        return jsonify(recipes)
      
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch recipes: {e}")

@app.route("/getRecipe/<int:recipe_id>")
def get_recipe(recipe_id):
    """Show a recipe."""
    
    if user_not_in_session():
        return redirect("/")
      
    if not_same_username(g.user.username):
        return redirect(f"/users/{session['username']}")
    
    check_api(API_KEY)
    url = f"{API_BASE_URL}/{recipe_id}/information"
    
    queryParameters = {
      'apiKey': API_KEY,
      'includedNutrition': "false"
    }
    
    try:
        response = requests.get(url, params=queryParameters)
        response.raise_for_status()
        
        recipeData = response.json()
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch recipes: {e}")
    
    return render_template(f"users/recipe.html", user=g.user, recipe=recipeData)
