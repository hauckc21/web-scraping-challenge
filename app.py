from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#create an instance of FLask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find a record of data in mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    #return tmeplate and data
    return render_template("index.html", mars=mars_dict)

@app.route("/scrape")
def scrape():
  
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

