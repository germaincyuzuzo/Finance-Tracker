from flask import Flask, render_template, request, redirect, url_for
from models import db, Income, Expense


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')

def index():
    incomes = Income.query.all()
    expenses = Expense.query.all()
    return render_template('index.html', incomes=incomes, expenses=expenses)


@app.route('/add', methods=['GET', 'POST'])

def add_entry():
    if request.method == 'POST':
        entry_type = request.form['type']
        amount = request.form['amount']
        source = request.form['source/category']

        if entry_type == 'income':
            new_income = Income(amount=amount, source=source)
            db.session.add(new_income)
        else:
            new_expense = Expense(amount=amount, category=source)
            db.session.add(new_expense)

        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template ('add_entry.html')

if __name__ == '__main__':
    app.run(debug=True)