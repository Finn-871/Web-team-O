import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_restful import Api, Resource
from models import db, User
from auth import require_api_key
from datetime import timedelta
from services import get_all_events, get_event

app = Flask(__name__)

db_folder = os.path.join(os.getcwd(), "database")
db_users_path = os.path.join(db_folder, "users.db")
db_keys_path = os.path.join(db_folder, "api_keys.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_users_path}'
app.config['SQLALCHEMY_BINDS'] = {'keys': f'sqlite:///{db_keys_path}'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRETKEY'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=7)

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
            "username": u.username,
            "staff": u.staff
        } for u in users])

        return jsonify(user_list)

    #add user
    @require_api_key
    def post(self):
        data = request.get_json()
        if not data or "fullname" not in data or "password" not in data or "username" not in data or "staff" not in data:
            return jsonify({"error": "Missing fields: fullname, password, staff"}), 400

        new_user = User(
            fullname=data["fullname"],
            username=data["username"],
            staff=data["staff"])
        new_user.set_password(data["password"])

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
        user.username = data["username"]
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

#moving across pages
@app.route('/')
def index():
    users = User.query.all()
    return render_template('login.html', users=users)

@app.route('/user-list')
def list():
    users = User.query.all()
    return render_template('user-list.html', users=users)

@app.route('/stu-home')
def stu_home():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    current_user = User.query.get(session['user_id'])
    events = get_all_events()   # get events from JSON

    return render_template('student_home.html', user=current_user, events=events)

#alter user database
@app.route('/add', methods=['POST'])
def add_user():
    fullname = request.form['name']
    password = request.form['password']
    username = request.form["username"]
    is_staff = 'staff' in request.form
    new_user = User(fullname=fullname, username=username, staff=is_staff)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username_attempt = request.form.get('username')
        password_attempt = request.form.get('password')

        print(f"Attempting login for: {username_attempt}")
        user = User.query.filter_by(username=username_attempt).first()

        if user:
            print(f"User found: {user.username}")
            if user.check_password(password_attempt):
                session.permanent = True
                session['user_id'] = user.id
                session['is_staff'] = user.staff

                return redirect(url_for('stu_home'))
            else:
                print("incorrect password")
        else:
            print("user not found")

    return redirect(url_for('index'))

@app.route('/student-calendar')
def student_calendar():
    return render_template('student_calendar.html')

@app.route('/student-event-details')
def student_event_detail():
    return render_template('student_event_details.html')

@app.route('/your-favourites')
def your_favourites():
    return render_template('your-favourites.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)

