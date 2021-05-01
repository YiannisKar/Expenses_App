from flask import Flask, render_template, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "mydatabase.db")
)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expensename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)



@app.route("/")
def add():
    return render_template('add.html')

@app.route('/expenses')
def expenses():
    expenses=Expense.query.all()
    total = 0
    total_business = 0
    total_other = 0
    total_food = 0
    total_entertainment = 0
    for expense in expenses:
        total += expense.amount
        if(expense.category == "business"):
            total_business += expense.amount
        elif(expense.category == "other"):
            total_other += expense.amount
        elif(expense.category == "food"):
            total_food += expense.amount
        elif(expense.category == "entertainment"):
            total_entertainment += expense.amount
        
    return render_template('expenses.html',expenses=expenses,total=total,total_business=total_business,total_food=total_food,total_other=total_other,total_entertainment = total_entertainment)

@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route("/updateexpense/<int:id>")
def updateexpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('/updateexpense.html', expense=expense)
    
        
@app.route('/edit', methods=['POST'])
def edit():
    id = request.form['id']
    date = request.form['date']
    expensename = request.form['expensename']
    category = request.form['category']

    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.expensename = expensename
    expense.category = category

    db.session.commit()
    return redirect('/expenses')



@app.route("/addexpense", methods=['POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    print(date + " " + expensename + " " + amount + " " + category)
    expense = Expense(
        date=date,
        expensename=expensename,
        amount=amount,
        category=category

    )
    db.session.add(expense)
    db.session.commit()
    print(expense)
    return redirect('/expenses')

if __name__ == "__main__":
    app.run(debug=True)


