from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1/test1'
app.config['JWT_SECRET_KEY'] = '8Bd9$q4}62_CLt33'
jwt = JWTManager(app)
mongo = PyMongo(app)
CORS(app)

from routes import user, jobs, cv

if __name__ == "__main__":
    app.run(debug = True, threaded = True)  
