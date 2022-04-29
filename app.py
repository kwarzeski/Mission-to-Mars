from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# homepage route
@app.route("/")
def index():
   # find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   # return an HTML template using an index.html
   return render_template("index.html", mars=mars)
   
# scrape route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   # newly scraped data
   mars_data = scraping.scrape_all()
   # .update_one(query_parameter, {"$set": data}, options)
   # inserting data, but not if an identical record already exists
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #  navigate the page back to root
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
