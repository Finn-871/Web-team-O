import os
import google_auth_oauthlib.flow
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_restful import Api, Resource
from models import db, User, Registration, Events
from auth import require_api_key
from datetime import timedelta
from services import get_all_events, get_event
from utils import add_event_to_google
from google.oauth2.credentials import Credentials

app = Flask(__name__)

db_folder = os.path.join(os.getcwd(), "database")
db_users_path = os.path.join(db_folder, "users.db")
db_events_path = os.path.join(db_folder, "events.db")
db_keys_path = os.path.join(db_folder, "api_keys.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_users_path}'
app.config['SQLALCHEMY_BINDS'] = {'keys': f'sqlite:///{db_keys_path}', 'events': f'sqlite:///{db_events_path}'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SECRETKEY'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=7)

db.init_app(app)
api = Api(app)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
if os.getenv('CODESPACE_NAME'):
    codespace_name = os.getenv('CODESPACE_NAME')
    PREFERRED_URL_SCHEME = 'https'
    app.config['SERVER_NAME'] = f"{codespace_name}-8000.app.github.dev"

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

#--------------------------------moving across pages------------------------------------
@app.route('/')
def index():
    users = User.query.all()
    return render_template('login.html', users=users)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/user-list')
def list():
    users = User.query.all()
    return render_template('user-list.html', users=users)

#student pages
@app.route('/student-calendar')
def student_calendar():
    return render_template('student_calendar.html')

@app.route('/student-event-details')
def student_event_details():
    event_id = request.args.get('id')
    event = get_event(event_id) if event_id else None
    return render_template('student_event_details.html', event=event)

@app.route('/student-home')
def student_home():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    current_user = User.query.get(session['user_id'])
    events = get_all_events()   # get events from JSON

    return render_template('student_home.html', user=current_user, events=events)

@app.route('/student-events')
def student_events():
    return render_template('student_calendar.html')

#staff pages
@app.route('/staff-attending-list')
def staff_attending_list():
    event_id = request.args.get('event_id')
    registrations = Registration.query.filter_by(event_id=event_id).all()
    users = [User.query.get(r.user_id) for r in registrations]
    return render_template('admin_attending_list.html', users=users)

@app.route('/staff-edit-event')
def staff_event_calendar():
    return render_template('admin_event_edit.html')

@app.route('/staff-event-details')
def staff_event_details():
    return render_template('admin_event_details.html')

@app.route('/staff-home')
def staff_home():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    current_user = User.query.get(session['user_id'])
    events = get_all_events()   # get events from JSON

    return render_template('admin_home.html', user=current_user, events=events)

#universal pages
@app.route('/your-favourites')
def your_favourites():
    return render_template('your-favourites.html')
    
#-----------------------------alter user databases-------------------------------
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

@app.route('/register-event', methods=['POST'])
def register_event():
    event_id = request.form.get('event_id')
    user_id = session.get('user_id')
    
    existing = Registration.query.filter_by(user_id=user_id, event_id=event_id).first()
    if not existing:
        reg = Registration(user_id=user_id, event_id=event_id)
        db.session.add(reg)
        db.session.commit()
    
    return redirect(url_for('student_home'))

#--------------------------------login logic------------------------------
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username_attempt = request.form.get('username')
        password_attempt = request.form.get('password')

        user = User.query.filter_by(username=username_attempt).first()

        if user:
            if user.check_password(password_attempt):
                session.permanent = True
                session['user_id'] = user.id
                session['is_staff'] = user.staff

                if user.staff == True:
                    return redirect(url_for('staff_home'))
                else:
                    return redirect(url_for('student_home'))
            else:
                print("incorrect password")
        else:
            print("user not found")

    return redirect(url_for('index'))

#----------------------Google Calendar---------------------------------------
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
@app.route('/authorise')
def authorise():
    session.permanent = True
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json', scopes=SCOPES)
    flow.redirect_uri = redirect_uri="https://psychic-space-fortnight-455wp766qpvfj6qv-8000.app.github.dev/oauth2callback"

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', code_challenge=None)
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json', scopes=SCOPES, state=state)
    flow.redirect_uri = "https://psychic-space-fortnight-455wp766qpvfj6qv-8000.app.github.dev/oauth2callback"
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['google_creds'] = credentials_to_dict(credentials)
    return redirect(url_for('student_event_details'))

@app.route('/sync-event/<int:id>')
def sync_event(id):
    event = Events.query.get(id)
    creds = session.get('google_creds')
    if not creds:
        return redirect(url_for('authorise'))

    creds = Credentials(**creds)

    add_event_to_google(event, creds)
    return redirect(url_for('student_event_details'))


def credentials_to_dict(credentials):
    return{
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes':credentials.scopes
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8000)

