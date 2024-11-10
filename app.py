from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import os
import matplotlib.pyplot as plt
import seaborn as sns
import io

app = Flask(__name__)

# Set the API key directly in the code to avoid issues with the environment variable
api_key = os.getenv('GOOGLE_API_KEY')  # Replace with your actual API key
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
        formatted_response = """
        <div style='font-family: Arial, sans-serif; font-size: 18px; line-height: 1.8; color: #333; text-align: left;'>

            <h2 style='color: #1a73e8; margin-bottom: 20px;'>Your Personalized Financial Advice</h2>

            <!-- Income Analysis Box -->
            <div style='border: 2px solid #4a90e2; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #d0e7fd; text-align: left;'>
                <h3 style='color: #2b6cb0; margin-bottom: 15px;'>Income Analysis</h3>
                <p>{income_response}</p>
            </div>

            <!-- Expense Analysis Box -->
            <div style='border: 2px solid #ff7043; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #ffe0b2; text-align: left;'>
                <h3 style='color: #ff7043; margin-bottom: 15px;'>Expense Analysis</h3>
                <p>{expense_response}</p>
            </div>

            <!-- Savings Plan Box -->
            <div style='border: 2px solid #4caf50; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #c8e6c9; text-align: left;'>
                <h3 style='color: #4caf50; margin-bottom: 15px;'>Savings Plan</h3>
                <p>{savings_response}</p>
            </div>

            <!-- Investment Advice Box -->
            <div style='border: 2px solid #7e57c2; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #d1c4e9; text-align: left;'>
                <h3 style='color: #7e57c2; margin-bottom: 15px;'>Investment Advice</h3>
                <p>{investment_response}</p>
            </div>

            <!-- Goal-Specific Financial Plan Box -->
            <div style='border: 2px solid #ffa726; border-radius: 8px; padding: 20px; margin-bottom: 25px; background-color: #ffe0b2; text-align: left;'>
                <h3 style='color: #ffa726; margin-bottom: 15px;'>Goal-Specific Financial Plan</h3>
                <p>{goal_response}</p>
            </div>

        </div>
        """.format(
            income_response=income_response.replace('#', '').replace('*', '').replace('\n', '</p><p>'),
            expense_response=expense_response.replace('#', '').replace('*', '').replace('\n', '</p><p>'),
            savings_response=savings_response.replace('#', '').replace('*', '').replace('\n', '</p><p>'),
            investment_response=investment_response.replace('#', '').replace('*', '').replace('\n', '</p><p>'),
            goal_response=goal_response.replace('#', '').replace('*', '').replace('\n', '</p><p>')
        )

        return jsonify({"advice": formatted_response})
    except AttributeError:
        return jsonify({"error": "Error: The method generate_content may not be supported in this library version."})
    except Exception as e:
        return jsonify({"error": str(e)})

sns.set_theme(style="darkgrid")

@app.route('/generate_plot')
def generate_plot():
    try:
        if not user_data['income'] or not user_data['expenses']:
            # If there's no income or expenses data
            img = io.BytesIO()
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#1f2937')
            ax.set_facecolor('#1f2937')
            ax.text(0.5, 0.5, "No data available for plot generation.", fontsize=12, ha='center', va='center', color='white')
            ax.axis('off')
            plt.close()
            img.seek(0)
            return send_file(img, mimetype='image/png')

        # Data for pie chart
        total_income = sum(item['amount'] for item in user_data['income'])
        total_expenses = sum(item['amount'] for item in user_data['expenses'])
        remaining_income = total_income - total_expenses

        # Ensure remaining income is not negative for proper visualization
        if remaining_income < 0:
            remaining_income = 0

        labels = ['Total Income', 'Total Expenses', 'Savings']
        sizes = [total_income, total_expenses, remaining_income]
        colors = ['#4caf50', '#ff7043', '#7e57c2']

        # Create the pie chart
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'color': "white"}
        )

        # Adjust the color of labels and percentages for better visibility
        for text in texts:
            text.set_color('white')
        for autotext in autotexts:
            autotext.set_color('white')

        # Set background and title color
        fig.patch.set_facecolor('#1f2937')
        ax.set_facecolor('#1f2937')
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
        ax.set_title("Income, Expenses, and Savings Breakdown", color='white')

        # Save plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight')
        img.seek(0)
        plt.close()
        return send_file(img, mimetype='image/png')

    except Exception as e:
        # Log the error and return an error message image
        print(f"Error in generate_plot: {e}")
        img = io.BytesIO()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#1f2937')
        ax.set_facecolor('#1f2937')
        ax.text(0.5, 0.5, "Error generating plot.", fontsize=15, ha='center', va='center', color='red')
        ax.axis('off')
        plt.close()
        img.seek(0)
        return send_file(img, mimetype='image/png')


@app.route('/generate_income_expense_plot')
def generate_income_expense_plot():
    try:
        if not user_data['income'] or not user_data['expenses']:
            img = io.BytesIO()
            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#1f2937')
            ax.set_facecolor('#1f2937')
            ax.text(0.5, 0.5, "No data available for plot generation.", fontsize=12, ha='center', va='center', color='white')
            ax.axis('off')
            plt.close()
            img.seek(0)
            return send_file(img, mimetype='image/png')

        income_descriptions = [item['description'] for item in user_data['income']]
        income_amounts = [item['amount'] for item in user_data['income']]
        expense_descriptions = [item['description'] for item in user_data['expenses']]
        expense_amounts = [item['amount'] for item in user_data['expenses']]

        descriptions = income_descriptions + expense_descriptions
        amounts = income_amounts + expense_amounts
        colors = ['#4caf50'] * len(income_amounts) + ['#ff7043'] * len(expense_amounts)

        fig, ax = plt.subplots()
        ax.bar(descriptions, amounts, color=colors)
        fig.patch.set_facecolor('#1f2937')
        ax.set_facecolor('#1f2937')
        ax.set_xlabel('Categories', color='white')
        ax.set_ylabel('Amount ($)', color='white', labelpad=20)  # Add padding to prevent cutoff
        ax.set_title('Income vs Expenses Breakdown', color='white')
        ax.tick_params(axis='x', colors='white', rotation=45)
        ax.tick_params(axis='y', colors='white')

        plt.tight_layout()  # Ensure that everything fits properly

        img = io.BytesIO()
        plt.savefig(img, format='png', facecolor=fig.get_facecolor(), bbox_inches='tight')
        img.seek(0)
        plt.close()
        return send_file(img, mimetype='image/png')

    except Exception as e:
        print(f"Error in generate_income_expense_plot: {e}")
        img = io.BytesIO()
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#1f2937')
        ax.set_facecolor('#1f2937')
        ax.text(0.5, 0.5, "Error generating plot.", fontsize=15, ha='center', va='center', color='red')
        ax.axis('off')
        plt.close()
        img.seek(0)
        return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
