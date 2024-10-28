from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/goal_tracker', methods=['GET', 'POST'])
def goal_tracker():
    if request.method == 'POST':
        # Handle user input here
        user_income = request.form['income']
        user_expenses = request.form['expenses']
        financial_goals = request.form['goal']
        # Redirect to advice page with user data
        return render_template('advice.html', income=user_income, expenses=user_expenses, goal=financial_goals)
    return render_template('goal_tracker.html')

if __name__ == '__main__':
    app.run(debug=True)

