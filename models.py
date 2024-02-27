"""Models for Recipe app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy(session_options={"expire_on_commit": False})

DEFAULT_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/832px-No-Image-Placeholder.svg.png"

class User(db.Model):
    """User"""
  
    __tablename__ = "users"
    
    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email} first_name={self.first_name} last_name={self.last_name}"
    
    id = db.Column(
      db.Integer(),
      primary_key=True
    )
    
    username = db.Column(
      db.String(20), 
      nullable=False, 
      unique=True
    )
    
    password = db.Column(
      db.Text, 
      nullable=False
    
    )
    email = db.Column(
      db.String(50), 
      nullable=False, 
      unique=True
    )
    
    first_name = db.Column(
      db.String(30),
      nullable=False
    )
    
    last_name = db.Column(
      db.String(30), 
      nullable=False
    )
    
    favorites = db.relationship("Favorite")
    
    #class methods
    @classmethod
    def signup(cls, username, password, email, first_name, last_name):
        """Sign up a user. 
        
        Hashes password and adds user to database.
        """
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
          username=username,
          password=hashed_pwd,
          email=email,
          first_name=first_name,
          last_name=last_name
        )
        
        db.session.add(user)
        return user
      
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct.
           Return user if valid: else return False."""
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False
      
    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


class Favorite(db.Model):
    """Favorite"""     
    
    __tablename__ = "favorites"
    
    def __repr__(self):
        return f"{self.id}, {self.recipe_id}, {self.recipe_title}, {self.user_id}"
    
    id = db.Column(
      db.Integer(),
      primary_key=True
    )
    
    recipe_id = db.Column(
      db.Integer(), 
      nullable=False, 
      unique=True
    )
    
    recipe_title = db.Column(
      db.Text(),
      nullable=False
    )
    
    recipe_img = db.Column(
      db.Text(),
      nullable=False,
      default=DEFAULT_IMAGE_URL
    )
    
    user_id = db.Column(
      db.Integer(),
      db.ForeignKey('users.id', ondelete='cascade'),
      nullable=False  
    )
    
     
      
def connect_db(app):
  """Connect to database."""
  
  db.app = app
  db.init_app(app)