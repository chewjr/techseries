# Import Flask and initialize a Flask application
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime

import datetime
import urllib, json, requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/techseries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app, resources={r"/foo": {"origins": "*"}})

class Goal(db.Model):
    __tablename__ = 'goal'

    user_id = db.Column(db.String, primary_key=True, nullable=False)
    goal_id = db.Column(db.String, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String, nullable = False)
    amount = db.Column(db.Float(precision=2), nullable = False)
    deadline = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, goal_id, created_at, category, amount, deadline):
        self.user_id = user_id
        self.goal_id = goal_id
        self.created_at = created_at
        self.category = category 
        self.amount = amount
        self.deadline = deadline


    def json(self):
        return {"user_id": self.user_id, "goal_id": self.goal_id, "created_at": self.created_at, "category": self.category, "amount": self.amount, "deadline": self.deadline}


# finding all goals belonging to a user_id
# all goals of user
@app.route("/goal/<string:user_id>", methods=["GET"])
def get_all_by_user_id(user_id):

    goal = Goal.query.filter_by(user_id = user_id)
    if goal:
        listOfgoal = []
        for goal in Goal.query.filter_by(user_id = user_id):
            res = {}
            res['goal_id'] = goal.goal_id
            res['created_at'] = goal.created_at
            res['category'] = goal.category
            res['amount'] = goal.amount
            res['deadline'] = goal.deadline
            listOfgoal.append(res)
        return jsonify({"goal": listOfgoal}), 200
        # return jsonify({"goal": [goal.json() for goal in goal.query.filter_by(user_id = user_id)]}), 200
    else:
        return jsonify({"message": "No goal found."}), 500


#adding goals
@app.route("/add_goal", methods =['POST'])
def add_goal_into_goal_db():
    try: 

        go = request.get_json()
        try:
            max_id = db.session.query(db.func.max(Goal.goal_id)).scalar()
            goal_id = max_id + 1
        except:
            goal_id = 1

        user_id = go["id"]
        created_at = datetime.now()
        category = go['category']
        amount = go['amount']
        deadline = go['deadline']

        # budget_exist = Budget.query.filter_by(user_id = user_id, created_at = created_at ).first()

        # if budget_exist:
        #     budget_exist_json = budget_exist.json()
        #     budget_exist_json = dict(budget_exist_json)
        #     # Budget_numshare = budget_exist_json['numshare'] 
        #     # budget_exist.numshare = int(Budget_numshare) + int(qty)
        #     Budget_totalprice = budget_exist_json['totalprice']
        #     budget_exist.totalprice = float(Budget_totalprice) + float(totalprice)
        #     budget_exist.Budgetprice = (float(Budget_totalprice) + float(totalprice)) / (budget_exist_json['numshare'] + int(qty))
            
            
        #     db.session.commit()
        #     # new entry
        #     return jsonify({"budget": [budget.json() for budget in Budget.query.filter_by(user_id = user_id, created_at = created_at)]}), 200

        # else:
        new_go = Goal(user_id, goal_id, created_at, category, amount, deadline)
        db.session.add(new_go)
        db.session.commit()
        # new entry
        #might need to change this to a string
        return jsonify({"message":"Success"}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the goal database."}) , 500




@app.route("/remove_goal", methods =['POST'])
def remove_goal_from_goal_db():

    try: 

        remove_go = request.get_json()

        user_id = remove_go["user_id"]
        goal_id = remove_go["goal_id"]
        

        goal_exist = Goal.query.filter_by(user_id=user_id, goal_id=goal_id).first()
        if goal_exist:
            Goal.query.filter_by(user_id = user_id, goal_id=goal_id).delete()
            # db.session.delete()  ##try this if .delete() doesnt work
            db.session.commit()
            return jsonify({"message": "Goal has been removed from goal database"}), 200
            # else:
            #     budget_exist.numshare -= qty
            #     budget_exist.totalprice = budget_exist.numshare * budget_exist.Budgetprice
            #     db.session.commit()
            #     return jsonify({"message": "Budget is removed from Budget database"}), 200
        else:
            return jsonify({"message":"This entry does not exist in the goal database."}) , 500    

    except:
        return jsonify({"message":"An error occurred removing this entry in the goal database."}) , 500


#edit goal

@app.route("/edit_goal", methods =['POST'])
def edit_goal_into_goal_db():
    try: 

        edit_goal = request.get_json()

        user_id = edit_goal["user_id"]
        goal_id = edit_goal["goal_id"]
        # created_at = edit_goal["created_at"]
        category = edit_goal['category']
        amount = edit_goal['amount']
        deadline = edit_goal['deadline']

        goal_exist = Goal.query.filter_by(user_id = user_id, goal_id = goal_id).first()

        if goal_exist:
            goal_exist.category = category
            goal_exist.amount = amount
            goal_exist.deadline = deadline

            db.session.commit()
            # new entry
            return jsonify({"goal": [goal.json() for goal in Goal.query.filter_by(user_id = user_id, goal_id = goal_id)]}), 200

        # else:
        #     new_bud = Stock(username,ticker, qty, stockprice, totalprice)
        #     db.session.add(new_bud)
        #     db.session.commit()
        #     # new entry
        #     return jsonify({"stock": [stock.json() for stock in Stock.query.filter_by(username = username, ticker = ticker)]}), 200

    except:
        return jsonify({"message":"An error occurred editing this entry in the goal database."}) , 500

if __name__ == '__main__':
    app.run(port=5003, debug=True) 
