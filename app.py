import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_restful import Api, Resource
from models import db, User
from auth import require_api_key

app = Flask(__name__)

db_folder = os.path.join(os.getcwd(), "database")
db_users_path = os.path.join(db_folder, "users.db")
db_keys_path = os.path.join(db_folder, "api_keys.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_users_path}'
app.config['SQLALCHEMY_BINDS'] = {'keys': f'sqlite:///{db_keys_path}'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class UserAPI(Resource):
    #get user
    @require_api_key
    def get(self):
        users = User.query.all()
        return([{
            "id": u.id,
            "fullname": u.fullname,
            "password": u.password,
            "staff": u.staff
        } for u in users])

        return jsonify(user_list)

    #add user
    @require_api_key
    def post(self):
        data = request.get_json()
        if not data or "fullname" not in data or "password" not in data or "staff" not in data:
            return jsonify({"error": "Missing fields: fullname, password, staff"}), 400

        new_user = User(
            fullname=data["fullname"],
            password=data["password"],
            staff=data["staff"])
        
        db.session.add(new_user)
        db.session.commit()
        return {"message": "New user added"}

    #update user
    @require_api_key
    def put(self):
        data = request.json
        user_id = data.get("id")
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}

        #update user details
        user.fullname = data["fullname"]
        user.password = data["password"]
        user.staff = data["staff"]

        db.session.commit()

        return {"message": "user updated"}

    #delete user
    @require_api_key
    def delete(self):
        data = request.json
        user_id = data.get("id")

        user = User.query.get(user_id)
        if not user:
            return {"error": "user not found"}

        db.session.delete(user)
        db.session.commit()

        return {"message": "user deleted"}

api.add_resource(UserAPI, "/api/users")

@app.route('/')
def index():
    users = User.query.all()
    return render_template('user-list.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    fullname = request.form['name']
    password = request.form['password']
    is_staff = 'staff' in request.form
    new_user = User(fullname=fullname, password=password, staff=is_staff)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)

