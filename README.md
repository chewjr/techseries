# FinanceMatics
A one stop application that aims to help ease youths into the world of personal finance. Our application consist of three main features

- Budget Tracking
- Goal Based Profile
- Education


### File Directory 
```
app
└───techseries.sql
└───requirements.txt
└───models
    └───budget.py
    └───user.py
    └───expenses.py
    └───goal.py
    └───news.py
└───templates
└───credits
README.md
```

Steps to run the application: 

- Load the database (techseries.sql)
- (optional) Set up your own virtual environment
- Run the command `pip install -r requirements.txt`
- Run the microservices (on separate windows)
  - `python budget.py`
  - `python user.py`
  - `python expenses.py`
  - `python goal.py`
  - `python news.py`
- Start the app journey by opening templates/login.html