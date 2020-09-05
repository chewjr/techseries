from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    occupation = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
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
def authenticate():
    data = request.get_json()
    id = data['id']
    password = data['password']

    result = {}
    user = user.query.filter_by(id=id).first()

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
def createuser():
    try: 

        user = request.get_json()

        user_id = user["id"]
        password = user["password"]
        created_at = 'hardcode' # hardcode
        first_name = user['first_name']
        last_name = user['last_name']
        occupation = user["occupation"]
        email = user['email']
        age = user['age']
        risk = user['risk']
        

        new_user = User(user_id, password, created_at, first_name, last_name, occupation, email, age, risk)
        db.session.add(new_user)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
        db.session.commit()
        # new entry
        return jsonify({"message":"Account successfully created"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the user database."}) , 500


if __name__ == "__main__": 
    app.run(port=5001, debug=True)
