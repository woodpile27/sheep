from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_DBNAME='sheep'
)
mongo = PyMongo(app)

@app.route('/')
def index():
    sheeps = mongo.db.sheeps.find()
    return render_template("index.html", sheeps=sheeps)

if __name__ == '__main__':
    app.run()
