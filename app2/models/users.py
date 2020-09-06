from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/techseries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "*"}})

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    risk = db.Column(db.Float, nullable=False)

    def __init__(self, id, password, created_at, first_name, last_name, occupation, email, age, risk):
        self.id = id
        self.password = password
        self.created_at = created_at
        self.first_name = first_name
        self.last_name = last_name
        self.occupation = occupation
        self.email = email
        self.age = age
        self.risk = risk


    def json(self): 
        return {"id": self.id, "password": self.password, "created_at": self.created_at,
                "first_name": self.first_name, "last_name": self.last_name, "occupation": self.occupation,
                "email": self.email, "age": self.age, "risk": self.risk}


# authenticate user when logging in
@app.route("/authenticate", methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def authenticate():
    data = request.get_json()
    id = data['id']
    password = data['password']

    result = {}
    user = User.query.filter_by(id=id).first()

    if user:
        if password == user.password:
            result['status'] = 'success'
        else: 
            result['status'] = 'error'
    else:
        result['status'] = 'error'
        result['message'] = 'User not found'
    print(result)
    return jsonify(result), 200


# create new user and insert into database
@app.route("/createuser", methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def createuser():
    result = {}
    try: 
        user = request.get_json()

        user_id = user["id"]
        password = user["password"]
        created_at = datetime.now()
        first_name = user['first_name']
        last_name = user['last_name']
        occupation = user["occupation"]
        email = user['email']
        age = user['age']
        risk = user['risk']

        query = User.query.filter_by(id=user_id).first()
        if query:
            result['status'] = 'error'
            result['message'] = 'User ID taken, please try another User ID'
            return jsonify(result), 200

        new_user = User(user_id, password, created_at, first_name, last_name, occupation, email, age, risk)
        db.session.add(new_user)
        db.session.commit()
        # new entry
        result['status'] = 'success'
        result['message'] = 'user successfully created'
        return jsonify(result), 200
    except:
        result['status'] = 'error'
        result['message'] = 'An error occurred creating this entry in the user database.'
        return jsonify(result) , 500

@app.route("/search/<string:user>")
def search_user(user):
    query = User.query.filter_by(id=user).first()
    return jsonify(query.json()), 200

if __name__ == "__main__": 
    app.run(port=5000, debug=True)
