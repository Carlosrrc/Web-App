from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Set the API key directly in the code to avoid issues with the environment variable
api_key = 'GOOGLE-API'  # Replace with your actual API key
genai.configure(api_key=api_key)

# Temporary storage for user data
user_data = {
    'income': [],
    'expenses': [],
    'goals': []
}

@app.route('/')
def home():
    return render_template('index.html', user_data=user_data)

@app.route('/add_income', methods=['POST'])
def add_income():
    description = request.json.get('income_description')
    amount = request.json.get('income_amount')
    if description and amount:
        user_data['income'].append({'description': description, 'amount': float(amount)})
    return ('', 204)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.json.get('expense_description')
    amount = request.json.get('expense_amount')
    if description and amount:
        user_data['expenses'].append({'description': description, 'amount': float(amount)})
    return ('', 204)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    description = request.json.get('goal')
    amount = request.json.get('goal_amount')
    if description and amount:
        user_data['goals'].append({'description': description, 'amount': float(amount)})
    return ('', 204)

@app.route('/financial_advice', methods=['POST'])
def financial_advice():
    # Use enhanced default data if user data is empty (for easier testing)
    if not user_data['income']:
        user_data['income'] = [
            {'description': 'Salary', 'amount': 5000.0},
            {'description': 'Freelancing', 'amount': 1200.0},
            {'description': 'Investments', 'amount': 800.0}
        ]
    if not user_data['expenses']:
        user_data['expenses'] = [
            {'description': 'Rent', 'amount': 1500.0},
            {'description': 'Utilities', 'amount': 300.0},
            {'description': 'Groceries', 'amount': 600.0},
            {'description': 'Entertainment', 'amount': 500.0}
        ]
    if not user_data['goals']:
        user_data['goals'] = [
            {'description': 'Buy a Car', 'amount': 30000.0},
            {'description': 'Vacation', 'amount': 5000.0},
            {'description': 'Emergency Fund', 'amount': 10000.0}
        ]

    total_income = sum(item['amount'] for item in user_data['income'])
    total_expenses = sum(item['amount'] for item in user_data['expenses'])
    remaining_income = total_income - total_expenses
    goals = ', '.join(f"{goal['description']} (${'{:.2f}'.format(goal['amount'])})" for goal in user_data['goals'])

    income_details = ', '.join(f"{income['description']} (${income['amount']:.2f})" for income in user_data['income'])
    expense_details = ', '.join(f"{expense['description']} (${expense['amount']:.2f})" for expense in user_data['expenses'])

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate distinct responses for each section with clear and direct prompts
        income_prompt = (
            f"Based on the following monthly income details: {income_details}, provide a straightforward income analysis. "
            f"Make suggestions for income growth or diversification that are practical. "
            f"Ensure the response is purely informative without any questions or requests for further information."
        )
        income_response = model.generate_content(income_prompt).text

        expense_prompt = (
            f"Based on the following monthly income (${total_income:.2f}) and monthly expenses: {expense_details}, provide an analysis of the spending pattern. "
            f"Identify if the expenses are high or low compared to the income, and provide realistic recommendations for reducing costs. "
            f"Ensure the response is direct and informative without any questions."
        )
        expense_response = model.generate_content(expense_prompt).text

        savings_prompt = (
            f"Given a monthly income of ${total_income:.2f} and monthly expenses of ${total_expenses:.2f}, formulate a savings plan that is realistic. "
            f"Include specific monthly saving recommendations and strategies to prepare for unexpected expenses. "
            f"Make the response actionable and straightforward without interactive components."
        )
        savings_response = model.generate_content(savings_prompt).text

        investment_prompt = (
            f"Based on the remaining monthly income of ${remaining_income:.2f} after covering expenses, suggest suitable investment options. "
            f"Provide specific short-term, medium-term, and long-term investment strategies. "
            f"Include examples of stocks, bonds, or ETFs where possible, and ensure the response does not contain follow-up questions or requests for more data."
        )
        investment_response = model.generate_content(investment_prompt).text

        goal_prompt = (
            f"Given the financial goal(s): {goals}, assess whether these goals are realistic based on the user's current monthly income (${total_income:.2f}) and expenses (${total_expenses:.2f}). "
            f"Provide an action plan to achieve these goals, or suggest alternative, more feasible goals if necessary. "
            f"Ensure the response is definitive without asking for more input."
        )
        goal_response = model.generate_content(goal_prompt).text

        # Updated HTML-based formatting for distinct sections, with improved readability
        formatted_response = f"""
        <div style='font-family: Arial, sans-serif; font-size: 18px; line-height: 1.8; color: #333; text-align: left;'>

            <h2 style='color: #1a73e8; margin-bottom: 20px;'>Your Personalized Financial Advice</h2>

            <!-- Income Analysis Box -->
            <div style='border: 2px solid #4a90e2; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #d0e7fd; text-align: left;'>
                <h3 style='color: #2b6cb0; margin-bottom: 15px;'>Income Analysis</h3>
                <p>{income_response.replace('#', '').replace('*', '').replace('\n', '</p><p>')}</p>
            </div>

            <!-- Expense Analysis Box -->
            <div style='border: 2px solid #ff7043; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #ffe0b2; text-align: left;'>
                <h3 style='color: #ff7043; margin-bottom: 15px;'>Expense Analysis</h3>
                <p>{expense_response.replace('#', '').replace('*', '').replace('\n', '</p><p>')}</p>
            </div>

            <!-- Savings Plan Box -->
            <div style='border: 2px solid #4caf50; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #c8e6c9; text-align: left;'>
                <h3 style='color: #4caf50; margin-bottom: 15px;'>Savings Plan</h3>
                <p>{savings_response.replace('#', '').replace('*', '').replace('\n', '</p><p>')}</p>
            </div>

            <!-- Investment Advice Box -->
            <div style='border: 2px solid #7e57c2; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #d1c4e9; text-align: left;'>
                <h3 style='color: #7e57c2; margin-bottom: 15px;'>Investment Advice</h3>
                <p>{investment_response.replace('#', '').replace('*', '').replace('\n', '</p><p>')}</p>
            </div>

            <!-- Goal-Specific Financial Plan Box -->
            <div style='border: 2px solid #ffa726; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #ffe0b2; text-align: left;'>
                <h3 style='color: #ffa726; margin-bottom: 15px;'>Goal-Specific Financial Plan</h3>
                <p>{goal_response.replace('#', '').replace('*', '').replace('\n', '</p><p>')}</p>
            </div>

        </div>
        """
        return jsonify({"advice": formatted_response})
    except AttributeError:
        return jsonify({"error": "Error: The method generate_content may not be supported in this library version."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
