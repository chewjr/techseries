from hmac import new
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import urllib, json, requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/techseries'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# cors = CORS(app, resources={r"/foo": {"origins": "*"}})

class Budget(db.Model):
    __tablename__ = 'budget'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float(precision=2), nullable = False)

    def __init__(self, id, user_id, created_at, amount):
        self.id = id
        self.user_id = user_id
        self.created_at = created_at
        self.amount = amount


    def json(self):
        return {"id": self.id, "user_id": self.user_id, "created_at": self.created_at, "amount": self.amount}


# finding all budget belonging to a user_id
# all budgets of user
@app.route("/budget/<string:user_id>", methods=["GET"])
def get_all_by_user_id(user_id):

    budget = Budget.query.filter_by(user_id=user_id)
    if budget:
        listOfbudget = []
        for budget in Budget.query.filter_by(user_id = user_id):
            res = {}
            res['created_at'] = budget.created_at
            res['created_at_words'] = budget.created_at.strftime("%B") + " " + str(budget.created_at.year)
            res['amount'] = budget.amount
            listOfbudget.append(res)
        return jsonify({"status": "success", "budget": listOfbudget}), 200
        # return jsonify({"budget": [budget.json() for budget in Budget.query.filter_by(user_id = user_id)]}), 200
    return jsonify({"status": "error", "message": "No budget found for user."}), 500


#adding budget
@app.route("/add_budget", methods =['POST'])
def add_budget_into_budget_db():
    try: 

        bud = request.get_json()

        user_id = bud["user_id"]
        # check if this month's budget has been created by user
        budget = Budget.query.filter_by(user_id=user_id)
        if budget:
            for budget in Budget.query.filter_by(user_id = user_id):
                if budget.created_at.month == datetime.now().month and budget.created_at.year == datetime.now().year:
                    return jsonify({"status": "error", "message": "User has already created budget for the month."}), 500

        created_at = datetime.now()
        amount = bud['amount']

        # get last id, and increment
        try:
            max_id = db.session.query(db.func.max(Budget.id)).scalar()
            id = max_id + 1
        except Exception:
            id = 1

        new_bud = Budget(id, user_id, created_at, amount)
        db.session.add(new_bud)
        db.session.commit()

        # new entry
        return jsonify({"status": 'success', 'message': 'Budget added to database'}), 201

    except:
        return jsonify({"status": "error", "message":"An error occurred creating this entry in the budget database."}) , 500


#remove budget
@app.route("/remove_budget", methods =['POST'])
def remove_budget_from_budget_db():

    try: 

        remove_bud = request.get_json()

        id = remove_bud["id"]

        budget_exist = Budget.query.filter_by(id=id).first()
        if budget_exist:
            Budget.query.filter_by(id=id).delete()
            # db.session.delete()  ##try this if .delete() doesnt work
            db.session.commit()
            return jsonify({"status": "success", "message": "Budget has been removed from budget database"}), 200
        else:
            return jsonify({"status": "error", "message":"This entry does not exist in the budget database."}), 500    
    except:
        return jsonify({"status": "error", "message":"An error occurred removing this entry in the budget database."}) , 500


#edit budget
@app.route("/edit_budget", methods =['POST'])
def edit_budget_into_budget_db():
    try: 

        bud = request.get_json()

        id = bud["id"]
        amount = bud['amount']

        bud_exist = Budget.query.filter_by(id=id).first()

        if bud_exist:
            bud_exist.amount = amount     
            db.session.commit()
            return jsonify({"status": "success", "message":"Successfully edited."}), 200

    except:
        return jsonify({"status": "error", "message":"An error occurred editing this entry in the budget database."}) , 500


# Check if budget has been created for the month
@app.route("/budget/month/<string:user_id>", methods=["GET"])
def get_month_budget(user_id):

    budget = Budget.query.filter_by(user_id=user_id)
    if budget:
        for budget in Budget.query.filter_by(user_id=user_id):
            if budget.created_at.month == datetime.now().month and budget.created_at.year == datetime.now().year:
                return jsonify({"status": "success", "budget": budget.json()}), 200
        return jsonify({"status": "error", "message": "User has not created budget for this month."}), 200
    return jsonify({"status": "error", "message": "User has no budget created for any month."}), 200




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
