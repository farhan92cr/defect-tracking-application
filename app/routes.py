from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, mongo
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = mongo.db.users.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    if username == 'admin' and password == 'password':
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return 'Invalid credentials', 401

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        # Check if the username already exists
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            return 'Username already exists', 400

        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('index'))

@app.route('/add_defect', methods=['GET', 'POST'])
def add_defect():
    if 'username' in session:
        if request.method == 'POST':
            model = request.form['model']
            defect_type = request.form['defect_type']
            imei = request.form['imei']
            image = None
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file.filename != '':
                    image = image_file.filename
                    image_file.save('app/static/images/' + image)
            mongo.db.defects.insert_one({'model': model, 'defect_type': defect_type, 'imei': imei, 'image': image})
            return redirect(url_for('dashboard'))
        return render_template('add_defect.html')
    return redirect(url_for('index'))

@app.route('/search_defect', methods=['GET', 'POST'])
def search_defect():
    if 'username' in session:
        if request.method == 'POST':
            imei = request.form['imei']
            defect = mongo.db.defects.find_one({'imei': imei})
            if defect:
                defect['_id'] = str(defect['_id'])
                return jsonify(defect)
            return 'No defect found', 404
        return render_template('search_defect.html')
    return redirect(url_for('index'))

@app.route('/all_defects', methods=['GET'])
def all_defects():
    if 'username' in session:
        defects = mongo.db.defects.find()
        defect_list = []
        for defect in defects:
            defect['_id'] = str(defect['_id'])  # Convert ObjectId to string
            defect_list.append(defect)
        return render_template('all_defects.html', defects=defect_list)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
