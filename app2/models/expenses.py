# Import Flask and initialize a Flask application
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

import datetime
import urllib, json, requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/techseries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)

class Expenses(db.Model):
    __tablename__ = 'expenses'

    user_id = db.Column(db.String, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, primary_key=True, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    amount = db.Column(db.Float(precision=2), nullable = False)

    def __init__(self, user_id, created_at, category, name, amount):
        self.user_id = user_id
        self.created_at = created_at
        self.category = category #hardcode
        self.name = name
        self.amount = amount


    def json(self):
        return {"user_id": self.user_id, "created_at": self.created_at, "category": self.category, "name": self.name, "amount": self.amount}


# finding all expenses belonging to a user_id
# returns all expenses of user
@app.route("/expenses/<string:user_id>", methods=["GET"])
def get_all_by_user_id(user_id):

    expenses = Expenses.query.filter_by(user_id = user_id)
    if expenses:
        listOfexpenses = []
        for expenses in Expenses.query.filter_by(user_id = user_id):
            res = {}
            res['created_at'] = expenses.created_at #hardcode?
            res['category'] = expenses.category
            res['name'] = expenses.name
            res['amount'] = expenses.amount
            listOfexpenses.append(res)
        return jsonify({"expenses": listOfexpenses}), 200
        # return jsonify({"expenses": [expenses.json() for expenses in expenses.query.filter_by(user_id = user_id)]}), 200
    else:
        return jsonify({"message": "No expenses found."}), 500


#adding expenses
@app.route("/add_expenses", methods =['POST'])
def add_expenses_into_expenses_db():
    try: 

        exp = request.get_json()

        user_id = exp["user_id"]
        created_at = exp["created_at"]
        category = exp['category']
        name = exp['name']
        amount = exp['amount']

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
        new_exp = Expenses(user_id, created_at, category, name, amount)
        db.session.add(new_exp)
        db.session.commit()
        # new entry
        return jsonify({"expenses": [expenses.json() for expenses in Expenses.query.filter_by(user_id = user_id)}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the expenses database."}) , 500




@app.route("/remove_expenses", methods =['POST'])
def remove_expenses_from_expenses_db():

    try: 

        remove_exp = request.get_json()

        user_id = remove_exp["user_id"]
        created_at = remove_exp["created_at"]
        

        expenses_exist = Expenses.query.filter_by(user_id=user_id, created_at=created_at).first()
        if expenses_exist:
            Expenses.query.filter_by(user_id = user_id, created_at=created_at).delete()
            # db.session.delete()  ##try this if .delete() doesnt work
            db.session.commit()
            return jsonify({"message": "Expenses has been removed from expenses database"}), 200
            # else:
            #     budget_exist.numshare -= qty
            #     budget_exist.totalprice = budget_exist.numshare * budget_exist.Budgetprice
            #     db.session.commit()
            #     return jsonify({"message": "Budget is removed from Budget database"}), 200
        else:
            return jsonify({"message":"This entry does not exist in the expenses database."}) , 500    

    except:
        return jsonify({"message":"An error occurred removing this entry in the expenses database."}) , 500


#edit expenses

@app.route("/edit_expenses", methods =['POST'])
def edit_expenses_into_expenses_db():
    try: 

        edit_exp = request.get_json()

        user_id = edit_exp["user_id"]
        created_at = edit_exp["created_at"]
        category = edit_exp['category']
        name = edit_exp['name']
        amount = edit_exp['amount']

        exp_exist = Expenses.query.filter_by(user_id = user_id, created_at = created_at).first()

        if exp_exist:
            exp_exist.category = category
            exp_exist.name = name
            exp_exist.amount = amount

            db.session.commit()
            # new entry
            return jsonify({"expenses": [expenses.json() for expenses in Expenses.query.filter_by(user_id = user_id, created_at = created_at)]}), 200
            
    except:
        return jsonify({"message":"An error occurred editing this entry in the expenses database."}) , 500

if __name__ == '__main__':
    app.run(port=5002, debug=True) 
