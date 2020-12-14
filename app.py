# ========================================
# Module 10: Web Scraping NASA
# 
# 10.5.1 Use Flask to Create a Web App
# ========================================


# ----------------------------------------
# Import Dependancies
# ----------------------------------------
# Flask Dependency
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping


# ----------------------------------------
# Set Up Flask
# ----------------------------------------
app = Flask(__name__)


# ----------------------------------------
# Use flask_pymongo to set up mongo connection
# ----------------------------------------
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL

# "mongodb://localhost:27017/mars_app" is the URI we'll be using 
# to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, 
# using port 27017, using a database named "mars_app".


# ----------------------------------------
# Set up App Route for the HTML Page
# ----------------------------------------
# Create Route -- tells Flask what to display at home page, index.html
@app.route("/")

# Add function 
def index():
   mars = mongo.db.mars.find_one()                  
   return render_template("index.html", mars=mars)

# **mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection 
# in our database, which we will create when we convert our Jupyter scraping 
# code to Python Script. We will also assign that path to the
# mars variable for later use.  

# **return render_template("index.html" tells Flask to return an HTML template
# using an index.html file. 
# We'll create this file after we build the Flask routes.

# , mars=mars) tells Python to use the "mars" collection in MongoDB


# ----------------------------------------
# Set up Scraping Route 
# *Review
# ----------------------------------------
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars       
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# The first line, @app.route(“/scrape”) defines the route that Flask will be using. 
# This route, “/scrape”, will run the function that we create just beneath it.

# The next lines allow us to access the database, scrape new data using our 
# scraping.py script, update the database, and return a message when 
# successful. Let's break it down.

# First, we define it with def scrape():.

# Then, we assign a new variable that points to our Mongo database: 
# mars = mongo.db.mars.

# Next, created a new variable to hold the newly scraped data: 
# mars_data = scraping.scrape_all(). In this line, we're referencing the 
# scrape_all function in the scraping.py file exported from Jupyter Notebook.

# Update the database using .update()

# ----------------------------------------
# Tell Flask to Run Code
# ----------------------------------------
if __name__ == "__main__":
   app.run()
