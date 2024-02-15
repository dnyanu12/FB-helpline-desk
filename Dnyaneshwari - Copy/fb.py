from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import facebook

app = Flask(_name_)
client = MongoClient('mongodb://localhost:27017/')
db = client['helpdesk']
users_collection = db['akash']

# Facebook app credentials
app_id ='1460215968173625'
redirect_uri = 'https://www.facebook.com/profile.php?id=100055813564681&mibextid=ZbWKwL'  # This shohttps://www.facebook.com/profile.php?id=100055813564681&mibextid=ZbWKwLuld be a URL on your domain where Facebook will redirect after authorization

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            # Login successful
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            return 'Invalid credentials'
    return render_template('login.html')
    @app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        if users_collection.find_one({'email': email}):
            return 'User already exists'
        users_collection.insert_one({'name': name, 'email': email, 'password': password})
        return redirect(url_for('login'))
    return render_template('registration.html')
    @app.route('/facebookintegration', methods=['GET', 'POST'])
def facebookintegration():
    if request.method == 'GET':
        # Redirect to Facebook login
        facebook_auth_url = f'https://www.facebook.com/v12.0/dialog/oauth?client_id={1460215968173625}&redirect_uri={https://www.facebook.com/profile.php?id=100055813564681&mibextid=ZbWKwL}&scope=manage_pages,pages_show_list'
        return redirect(facebook_auth_url)
    
    elif request.method == 'POST':
        # Handle the Facebook page connection or disconnection logic here
        action = request.form['action']
        if action == 'disconnect':
            # Implement Facebook page disconnection logic here
            print('Disconnecting Facebook Page...')
            return 'Disconnected from Facebook'
        else:
            return 'Invalid action'
    
    return render_template('facebook_integration.html')

@app.route('/facebook_callback')
def facebook_callback():
    code = request.args.get('code')
    if code:
        graph = facebook.GraphAPI()
        access_token = graph.get_access_token_from_code(code, redirect_uri, app_id, app_secret)
        # Use the access_token to interact with the Facebook Graph API
        graph = facebook.GraphAPI(access_token=access_token, version='12.0')
        # Example: Get user's pages
        pages = graph.get_object('me/accounts')
        # Process the pages data as needed
        return 'Connected to Facebook'
    else:
        return 'Failed to connect to Facebook'
if _name_ == '_main_':
    app.run(debug=True)
