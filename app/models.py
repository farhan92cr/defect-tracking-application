from app import mongo

def save_defect(data):
    defects = mongo.db.defects
    defects.insert_one(data)

def get_defect_by_imei(imei):
    defects = mongo.db.defects
    return defects.find_one({'imei': imei})

def get_all_defects():
    defects = mongo.db.defects
    return defects.find()
