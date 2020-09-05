# Import Flask and initialize a Flask application
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

import datetime
import urllib, json, requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)

class Budget(db.Model):
    __tablename__ = 'budget'

    user_id = db.Column(db.String(20), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, primary_key=True, nullable=False)
    category = db.Column(db.String(30), nullable = False)
    name = db.Column(db.String(30), nullable = False)
    amount = db.Column(db.Float, nullable = False)

    def __init__(self, user_id, created_at, category, name, amount):
        self.user_id = user_id
        self.created_at = created_at
        self.category = category
        self.name = name
        self.amount = amount


    def json(self):
        return {"user_id": self.user_id, "created_at": self.created_at, "category": self.category, "name": self.name, "amount": self.amount}


# finding all budget belonging to a user_id
# all budgets of user
@app.route("/budget/<string:user_id>", methods=["GET"])
def get_all_by_user_id(user_id):

    budget = Budget.query.filter_by(user_id = user_id)
    if budget:
        listOfbudget = []
        for budget in Budget.query.filter_by(user_id = user_id):
            res = {}
            res['created_at'] = budget.created_at #hardcode?
            res['category'] = budget.category
            res['name'] = budget.name
            res['amount'] = budget.amount
            listOfbudget.append(res)
        return jsonify({"budget": listOfbudget}), 200
        # return jsonify({"budget": [budget.json() for budget in Budget.query.filter_by(user_id = user_id)]}), 200
    else:
        return jsonify({"message": "No budget found."}), 500


#adding budget
@app.route("/add_budget", methods =['POST'])
def add_budget_into_budget_db():
    try: 

        bud = request.get_json()

        user_id = bud["user_id"]
        created_at = bud["created_at"]
        category = bud['category']
        name = bud['name']
        amount = bud['amount']


        new_bud = Budget(user_id, created_at, category, name, amount)
        db.session.add(new_bud)
        db.session.commit()

        # new entry
        # maybe change this to a string, might not need to get json query
        return jsonify({"budget": [budget.json() for budget in Budget.query.filter_by(user_id = user_id)}), 200

    except:
        return jsonify({"message":"An error occurred creating this entry in the budget database."}) , 500



#remove budget
@app.route("/remove_budget", methods =['POST'])
def remove_budget_from_budget_db():

    try: 

        remove_bud = request.get_json()

        user_id = remove_bud["user_id"]
        created_at = remove_bud["created_at"]
        

        budget_exist = Budget.query.filter_by(user_id=user_id, created_at=created_at).first()
        if budget_exist:
            Budget.query.filter_by(user_id = user_id, created_at=created_at).delete()
            # db.session.delete()  ##try this if .delete() doesnt work
            db.session.commit()
            return jsonify({"message": "Budget has been removed from budget database"}), 200

        else:
            return jsonify({"message":"This entry does not exist in the budget database."}) , 500    

    except:
        return jsonify({"message":"An error occurred removing this entry in the budget database."}) , 500

#edit budget

@app.route("/edit_budget", methods =['POST'])
def edit_budget_into_budget_db():
    try: 

        bud = request.get_json()

        user_id = bud["user_id"]
        created_at = bud["created_at"]
        category = bud['category']
        name = bud['name']
        amount = bud['amount']

        bud_exist = Budget.query.filter_by(user_id = user_id, created_at = created_at ).first()

        if bud_exist:
            # bud_exist_json = bud_exist.json()
            # bud_exist_json = dict(bud_exist_json)
            bud_exist.category = category
            bud_exist.name = name
            bud_exist.amount = amount
            # bud_exist.numshare = int(stock_numshare) + int(qty)
            # stock_totalprice = bud_exist_json['totalprice']
            # bud_exist.totalprice = float(stock_totalprice) + float(totalprice)
            # bud_exist.stockprice = (float(stock_totalprice) + float(totalprice)) / (bud_exist_json['numshare'] + int(qty))
            
            
            db.session.commit()
            # new entry
            return jsonify({"message":"Successfully edited."}), 200

    except:
        return jsonify({"message":"An error occurred editing this entry in the budget database."}) , 500







# retrieving all Budget with the cid and created_at from json request (sell) and checking if
# the qty user wants to sell is less than or equals to the qty he owns
# @app.route("/hasEnoughBudget", methods=['POST'])
# def hasEnoughBudget():
   
#     check_Budget = request.get_json()
#     user_id = check_Budget['user_id']
#     created_at = check_Budget['created_at']
    
#     Budget = Budget.query.filter_by(user_id=user_id, created_at=created_at).first()
    
#     if Budget:
        
#         Budget = Budget.json()
#         Budget = dict(Budget)
        
#         user_qty = Budget["numshare"]
        
#         if user_qty >= qty:
#             return jsonify({"hasEnoughBudget": "True"}), 200
#     return jsonify({"hasEnoughBudget": "False"}), 500

# @app.route("/retrieve_BudgetQty", methods=['GET'])
# def get_qty_by_user_id_created_at():
#     user_id = request.args.get('user_id')
#     created_at = request.args.get('created_at')
#     Budget = Budget.query.filter_by(user_id=user_id, created_at=created_at).first()
#     if Budget:    
#         Budget = Budget.json()
#         Budget = dict(Budget)
        
#         user_qty = Budget["numshare"]
#         return jsonify({"numshare": user_qty}), 200
#     return jsonify({"status": "error", "message": "No Budget found for user"}), 500
    

if __name__ == '__main__':
    app.run(port=5004, debug=True)
