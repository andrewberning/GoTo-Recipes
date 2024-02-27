# Project Proposal

My first Capstone Project is a Recipe Food site using the [Spoonacular API](https://spoonacular.com/food-api). Users can register or login to their account and search for food recipes based on titles of recipes in the API. Users have an option to get a set of random recipes. Also, users can save and delete recipes to their favorites list.

| Project    | Description                 |
| ---------- | --------------------------- |
| Goal       | The goal is to be able to search for recipes by the recipe title. Get a random number of recipes. Save recipes to a Favorites list. |
| Type       | This will be a website but it has the potential to become a mobile app. | 
| Tech Stack | The tech stack I will be using for this application is Python/Flask, Jinja, WTForms, PostgreSQL, SQLAlchemy, Javascript, HTML, CSS. | 
| Users      | Users who visit this site would be anyone looking to find recipes by title. |
| Data       | The data I plan on using comes from the “Spoonacular API”. It will contain the names of recipes, thier id's from the API, short descriptions of those recipes, and the URL to the full recipe. |
| Functionality | Users can: <ul><li>Register an account</li><li>Login</li><li>Search for Recipes</li><li>Get 10 random recipes</li><li>Save recipes to favorites list</li><li>Delete recipes from favorites list</li><li>Logout</li></ul>
| Stretch Goals | A feature that allows the creation of many different lists to separate recipes. Example: Dinner list, Vegan list, etc.<br/> A feature for users to comment on recipes and show the user other comments. |

# Breaking down your project

| Task Name                   | Description                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| Source Your Data            | The source for my data will be coming from the [Spoonacular API](https://spoonacular.com/food-api)  |
| Design Database schema      | The models used for my database will consit of: <ol><li>A User model:<ul><li>id as PK</li><li>username</li><li>password</li><li>email</li><li>first_name</li><li>last_name</li><li>favorites that has a relationship with "favorites" table</li></li></ul><li>A Favorite model<ul><li>id as PK</li><li>recipe_id as recipe id from the API</li><li>recipe_title as recipe title</li><li>user_id as FK to User</li></ul></li><ol> |
| User Flows                  | The user flows for this website will be: <ol><li>A login page for existing users to login</li><li>A register page for new users to signup</li><li>A home page where users can search for recipes by recipe title:<ul><li>After clicking the search button with a query, the first 10 recipes load</li><li>If the user wants to view more recipes from their search, they can click the view more button at the end of the list to do so</li><li>Users can also click the Random Recipes button to get 10 random recipes from the API</li></ul></li><li>A single recipe page: <ul><li>Show the title of the recipe, an image, a short description of the recipe</li><li>Also, buttons to go to the full recipe website, return to search, and go to favorites</li></ul></li><li>A favorites page that shows all of the users favorite recipes</li><li>Logout</li><ol> |
| Set up backend and database | Configure the environmental variables on your framework of choice for development and set up database.<br/>I am using Python/Flask for my backend and connecting it to PostgreSQL database.| 
| Set up frontend             | Set up frontend framework of choice and link it to the backend with a simple API call for example.<br/>I am using simple HTML, CSS, and Javascript with Jinja templating. Also WTForms for my login/register forms.
| User Authentication         | Fullstack feature - ability to authenticate (login and sign up) as a user. User will be able to login on the frontend by entering username and password. User will be able to register an account on the frontend by entering username, password, email, first name, and last name. If user successfully logs in or signs up, user will be authenticated and logged in! |

