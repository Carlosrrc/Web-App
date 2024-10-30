from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for goals and user data
user_data = {
    'income': None,
    'expenses': None,
    'goals': []
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/income_expenses', methods=['GET', 'POST'])
def income_expenses():
    if request.method == 'POST':
        user_data['income'] = float(request.form.get('income'))
        user_data['expenses'] = float(request.form.get('expenses'))
        return redirect(url_for('goal_tracker'))
    return render_template('income_expenses.html')

@app.route('/goal_tracker', methods=['GET', 'POST'])
def goal_tracker():
    if request.method == 'POST':
        description = request.form.get('goal')
        amount = request.form.get('amount')
        goal = {'id': len(user_data['goals']) + 1, 'description': description, 'amount': float(amount)}
        user_data['goals'].append(goal)
        return redirect(url_for('goal_tracker'))
    return render_template('goal_tracker.html', goals=user_data['goals'])

@app.route('/goal_tracker/delete/<int:goal_id>', methods=['POST'])
def delete_goal(goal_id):
    user_data['goals'] = [goal for goal in user_data['goals'] if goal['id'] != goal_id]
    return ('', 204)

@app.route('/financial_advice')
def financial_advice():
    income, expenses = user_data['income'], user_data['expenses']
    if income and expenses:
        available_income = income - expenses
        recommended_savings = available_income * 0.2
        advice = f"Based on your income of ${income:.2f} and expenses of ${expenses:.2f}, we recommend saving approximately ${recommended_savings:.2f} per month."
    else:
        advice = "Please enter your income and expenses in the Income & Expenses section to receive personalized advice."
    return render_template('advice.html', financial_advice=advice)

if __name__ == '__main__':
    app.run(debug=True)



