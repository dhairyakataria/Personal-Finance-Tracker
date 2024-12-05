# Personal Finance Tracker

This is a personal finance tracker web application built with **Flask**, **PostgreSQL**, and **Bootstrap 5**. The app allows users to manage their finances, track expenses, view reports, and analyze spending patterns. Users can log in, add accounts and transactions, and view dashboards with spending insights.

## Features

- **User Authentication**: Users can register, log in, and manage their accounts.
- **Account Management**: Users can add, edit, and delete accounts (e.g., bank accounts, wallets).
- **Transaction Management**: Users can track their transactions (income and expenses) with categories and subcategories.
- **Spending Analysis**: Users can view spending trends by category, track income vs. expenses, and monitor their remaining balance.
- **Dashboard**: A dynamic dashboard that shows total income, total expenses, and remaining balance.
- **Responsive Design**: The application is built with Bootstrap 5 to be responsive and user-friendly.

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, CSS (Bootstrap 5)
- **Database**: PostgreSQL (can be switched to other databases like MySQL)
- **Authentication**: Flask-Login, Flask-Bcrypt (password hashing)
- **Data Visualization**: Chart.js (for displaying spending and income vs. expense charts)

## Usage

1. **Register**: Create a new account by filling out the registration form.
2. **Login**: After registration, log in using your email and password.
3. **Manage Accounts**: Add bank accounts or wallets where you track your finances.
4. **Add Transactions**: Track income and expenses by adding transactions.
5. **Dashboard**: View your financial summary with charts displaying income vs. expenses and spending by category.

## File Structure

```plaintext
personal-finance-tracker/
│
├── app/
│   ├── __init__.py           # Initialize Flask app
│   ├── models.py             # Database models (User, Account, Transaction, etc.)
│   ├── routes.py             # Application routes
│   ├── forms.py              # Flask forms (for handling user inputs)
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Register page
│   │   ├── add_transaction.html # Add transaction form
│   │   ├── dashboard.html    # Dashboard page
│   │   ├── view_transaction.html # View Transaction page
│   └── static/               # Static files (CSS, JS, images)
│       └── css/              # Custom CSS files
│       └── js/               # JavaScript files (for charts)
│
├── run.py                    # To run flask app
├── config.py                 # Configuration file (app settings, DB URI, etc.)
├── requirements.txt          # Python dependencies
├── populate_defaults.py      # Script for adding default categories/subcategories
└── README.md                 # This file


## Database Models

### User
- **user_id**: Primary Key
- **name**
- **email**
- **password_hash**

### Account
- **account_id**: Primary Key
- **user_id**: Foreign Key to User
- **account_name**
- **account_type**
- **balance**

### Transaction
- **transaction_id**: Primary Key
- **account_id**: Foreign Key to Account
- **category_id**: Foreign Key to Category
- **subcategory_id**: Foreign Key to Subcategory
- **amount**
- **transaction_date**
- **transaction_type**: income/expense
- **description**

### Category
- **category_id**: Primary Key
- **name**

### Subcategory
- **subcategory_id**: Primary Key
- **category_id**: Foreign Key to Category
- **name**

## Features & Future Enhancements

- **Budget Tracking**: Allow users to set and track their monthly/annual budgets.
- **AI Integration**: Integrate with AI (like OpenAI's GPT) to provide financial advice based on spending patterns.
- **Bank API Integration**: Implement integration with bank APIs like Plaid to automatically import transactions.
- **Cloud Deployment**: Host the application on cloud platforms like Heroku, AWS, or Azure.

## Acknowledgements

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Chart.js Documentation](https://www.chartjs.org/)
