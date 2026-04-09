import os
from flask import Flask 
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_folder = os.path.join(os.getcwd(), "data")
db_path = os.path.join(db_folder, "users.db")

os.makedirs(db_folder, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_folder}/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0', port=8000)