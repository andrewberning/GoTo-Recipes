# Capstone Project One

[GoToRecipes](https://goto-recipes.onrender.com) is LIVE!!!

## Project Description
My first Capstone Project is called "GoTo Recipes". It is a Recipe Food website using the [Spoonacular API](https://spoonacular.com/food-api) to get data about recipes. Users can register or login to their account. Search for recipes based on the type of food (e.g. pasta or burgers). Users also have an extra option to get a set of random recipes. Users can choose to save recipes to their favorites list and delete them as well.

## User Types
Users who visit this site would be anyone looking to find recipes and save them for future reference.

## User Flow
The user flows for this website will be: <ol><li>A login page for existing users to login</li><li>A register page for new users to signup</li><li>A home page where users can search for recipes by food type:<ul><li>After clicking the search button with a query, the first 10 recipes load</li><li>If the user wants to view more recipes from their search, they can click the "view more" button at the end of the list to do so</li><li>Users can also click the Random Recipes button to get 10 random recipes from the API</li></ul></li><li>A single recipe page: <ul><li>Show the title, image, and a short description of the recipe</li><li>Also, buttons to go to the full recipe website, return to search, and go to favorites</li></ul></li><li>A favorites page that shows all of the users favorite recipes: <ul><li>User can click to see single recipe page</li><li>Delete recipe from list</li></ul></li><li>Logout</li></ol> 

## API Notes
The [Spoonacular API](https://spoonacular.com/food-api) is very easy to use for this website. You have to use an API key to make calls to their API. You must create an account with Spoonacular to obtain one. Signup was easy and their documentation is great. This API allows you to do many things. The possibilites are endless. Check them out!

## Tech Stack
The tech stack I used for this website consisted of Python, Flask, Jinja, WTForms, PostgreSQL, SQLAlchemy, Javascript, HTML, CSS.

## Getting Started
These instructions should get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
- Need Python 3.x
- pip3

### Installation
1. Clone the GoToRecipes [repo] (https://github.com/andrewberning/GoTo-Recipes.git) 
2. In terminal, navigate to project directory using "$ cd my-project"
3. Create your virtual environment with "$ python3 -m venv venv"
4. In terminal, navigate to your virtual environment (venv) with "$ source venv/bin/activate"
5. Install dependencies with "$ pip3 install -r requirements.txt"

### Running the Application
Be sure you are in your virtual environment. In your project folder, the command is "$ source venv/bin/activate"
To run this application, use the command "$ flask run" for developer mode.
If you would like to run in debug mode, use "$ flask run --debug". This is also in developer mode.
Use ctrl+C to quit the application.
  
### Configuring the Database
Change the database URI to what database type you will be using. 
I am using PostgreSQL for my application. 
Locally, create a database and use the name of the database in the URI like so,"app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipe'". 
In this case, the database name is "recipe". Replace "recipe" with your database name.
##### NOTE
When you depoloy, you must change the value of the SQLALCHEMY_DATABASE_URI to your new database url. It will be the same DATABASE URL you use when your are deploying to Render. More on this later.

### Schema Design
![GoToRecipes_SchemaDesign](https://github.com/andrewberning/GoTo-Recipes/assets/102753394/d4bc4a2d-7755-4b5e-86b8-8c241eea1958)

### Depoloyment
I am using Render to deploy this application and ElephantSQL for my database. I am using the free tier for both. 
  #### ElephantSQL
   - Create an account with ElephantSQL using GitHub.
   - Select the US-West-1 Region and the Tiny Turtle for free tier.
   - Confirm and create
   - Click on new instance and make note of the URL for your database. You will need it for Seeding your new instance database and for Render.
   - You should build your new instance much like your database you have locally.
     - In terminal, in you project folder, use the command "$ pg_dump -O recipe | psql (elephantsql url here)"
       - "recipe" is your local database you are seeding from. If your database name is different, change it accordingly.
       - "(elephantsql url here)" is the url noted above. Paste the url without the parentheses.
    - To check your database instance, use "$ psql (elephantsql url here). You can now use regular queries to verify your database was seeded properly.

  #### Render
  ##### Setting up your app
   -  You must install gunicorn via pip in your virtual environment of your project.
   -  Be sure you have your project on your GitHub.
   -  Create your account on Render with your GitHub.
   -  Create a new instance of "Web Service".
   -  Connect to your repository on GitHub.
   -  Make sure the start command is "gunicorn app:app
   -  Enter your environmental variables:
      -  DATABASE_URL: this will be that URL from ElephantSQL. Be sure you change "postgres:" -> "postgresql:" if you are using postgreSQL, like I did.
      -  SECRET_KEY: anything you want. Long and random is best!
      -  PYTHON_VERSION: 3:X:X - whichever version you are using
   - Choose "Create Web Service"
  ##### NOTE
   - If you have your API Key in a separate file and have it in your .gitignore (like I do), you have to tell Render about this file.
     - Below your "Evironment Variables" in the "Environments" tab, there is a section called "Secret Files". 
     - You must add the specific file name (e.g "keys.py") and what is in the file to go into "Contents" and click "Save Changes"
  
  #### Debuggin app
  - In the dashboard, you can view the logs.
  
  #### Updating app
  - When you push your GitHub repo, it will automatically redeploy your site.
  - You can turn it off in the settings.

### Testing
To test you must be in your virtual environment.
Test commands for terminal are provided at the top of the each test file.
  
### 

## Extra Notes
If the website takes a while to run, be patient. It is on the free tier of Render. <br/> For the Spoonacular service, I am also using the free tier. If there is an error code 402, this means no more calls to the API can be made until the quota resets (Quota resets daily at midnight UTC, check back tomorrow). 


## Summary
Thank you for checking out my first Capstone Project. If you have any question or comments. You can check out my profile on [LinkedIn](https://www.linkedin.com/in/andrew-berning?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BRJRwDTGYQsutUBc306VNaQ%3D%3D). Let me know what you think!
