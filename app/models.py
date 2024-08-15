from app import mongo
from werkzeug.security import generate_password_hash

def save_defect(data):
    defects = mongo.db.defects
    defects.insert_one(data)

def get_defect_by_imei(imei):
    defects = mongo.db.defects
    return defects.find_one({'imei': imei})

def get_all_defects():
    defects = mongo.db.defects
    return defects.find()

def save_user(username, password):
    users = mongo.db.users
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    users.insert_one({'username': username, 'password': hashed_password})
