# Smart Finances

A web app that gives personalised financial advice using AI. Made during my exchange semester at Nanyang Technological University (Singapore), as part of the minor in Programming, Artificial Intelligence and Finance.

## What it does

- You enter your monthly income, expenses and savings goals.
- The app sends this data to Google's Gemini model, which writes advice in five parts: income, expenses, a savings plan, investment ideas and a plan for each goal.
- It draws a chart of income against expenses (Matplotlib/Seaborn).

## Built with

- Python and Flask (backend)
- Google Gemini API (`google-generativeai`)
- HTML, Tailwind CSS and JavaScript (frontend)
- Deployed on Render with Gunicorn

## Run it locally

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY=your_key_here
python app.py
```

Then open http://127.0.0.1:5000.

Note: the app keeps data in memory only, so it resets when the server restarts.
