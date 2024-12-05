from flask import Blueprint, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, AccountForm, TransactionForm, EditAccountForm
from .models import User, Account, Transaction, Category, Subcategory
from . import db, bcrypt, login_manager

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Check if the user exists
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            # Login user
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            # Flash error message for invalid credentials
            flash('Invalid email or password.', 'danger')

    return render_template("login.html", form=form)


@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the email is already in use
        if User.query.filter_by(email=form.email.data).first():
            flash("Email is already registered. Please log in or use another email.", "danger")
            return redirect(url_for("main.register"))

        # Hash the password and create a new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(name=form.name.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully." "success")
    return redirect(url_for("main.login"))


@main.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(
            account_name=form.account_name.data,
            account_type=form.account_type.data,
            balance=form.balance.data,
            user_id=1
        )
        db.session.add(account)
        db.session.commit()
        flash('Account added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_account.html', form=form)


@main.route('/view_transactions', methods=['GET'])
@login_required
def view_transactions():
    # Fetch transactions for the logged-in user
    transactions = (
        db.session.query(
            Transaction.transaction_date,
            Account.account_name.label("account_name"),
            Category.name.label('category_name'),
            Subcategory.name.label('subcategory_name'),
            Transaction.amount,
            Transaction.transaction_type,
            Transaction.description,
            Transaction.currency
        )
        .join(Account, Transaction.account_id == Account.account_id)
        .join(Category, Transaction.category_id == Category.category_id)
        .join(Subcategory, Transaction.subcategory_id == Subcategory.subcategory_id)
        .filter(Account.user_id == current_user.user_id)
        .all()
    )

    # Print transactions to the terminal
    print("\n--- Transactions ---")
    for transaction in transactions:
        print(
            f"Date: {transaction.transaction_date}, "
            f"Account: {transaction.account_name}, "
            f"Category: {transaction.category_name}, "
            f"Subcategory: {transaction.subcategory_name}, "
            f"Amount: {transaction.amount}, "
            f"Type: {transaction.transaction_type}, "
            f"Description: {transaction.description}, "
            f"Currency: {transaction.currency}"
        )
    print("--- End of Transactions ---\n")

    return render_template('view_transactions.html', transactions=transactions)

@main.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    # Populate accounts and categories dropdowns
    form.account.choices = [(acc.account_id, acc.account_name) for acc in Account.query.all()]
    form.category.choices = [(cat.category_id, cat.name) for cat in Category.query.all()]
    form.subcategory.choices = [(sub.subcategory_id, sub.name) for sub in Subcategory.query.all()]

    print(form.account.data, form.category.data, form.subcategory.data, form.amount.data, form.transaction_date.data, form.transaction_type.data, form.description.data)
    if form.validate_on_submit():
        transaction = Transaction(
            account_id=form.account.data,
            category_id=form.category.data,
            subcategory_id=form.subcategory.data,
            amount=form.amount.data,
            transaction_date=form.transaction_date.data,
            transaction_type=form.transaction_type.data,
            description=form.description.data,
            currency="INR"
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.view_transactions'))
    return render_template('add_transaction.html', form=form)


@main.route('/get_subcategories/<int:category_id>', methods=['GET'])
@login_required
def get_subcategories(category_id):
    subcategories = Subcategory.query.filter_by(category_id=category_id).all()
    subcategories_data = [{"id": sub.subcategory_id, "name": sub.name} for sub in subcategories]
    return jsonify(subcategories_data)


from collections import defaultdict

@main.route('/dashboard')
@login_required
def dashboard():
    # Financial summary
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.transaction_type == 'income',
        Transaction.account_id.in_([acc.account_id for acc in Account.query.filter_by(user_id=current_user.user_id)])
    ).scalar() or 0

    total_expenses = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.transaction_type == 'expense',
        Transaction.account_id.in_([acc.account_id for acc in Account.query.filter_by(user_id=current_user.user_id)])
    ).scalar() or 0

    total_balance = db.session.query(db.func.sum(Account.balance)).filter(
        Account.user_id == current_user.user_id
    ).scalar() or 0
    remaining_balance = total_balance + total_income - total_expenses
    # Recent transactions
    recent_transactions = (
        db.session.query(
            Transaction.transaction_date,
            Account.account_name.label('account_name'),
            Category.name.label('category_name'),
            Subcategory.name.label('subcategory_name'),
            Transaction.amount,
            Transaction.transaction_type,
            Transaction.description,
            Transaction.currency
        )
        .join(Account, Transaction.account_id == Account.account_id)
        .join(Category, Transaction.category_id == Category.category_id)
        .join(Subcategory, Transaction.subcategory_id == Subcategory.subcategory_id)
        .filter(Account.user_id == current_user.user_id)
        .order_by(Transaction.transaction_date.desc())
        .limit(5)
        .all()
    )

    # Data for charts
    spending_by_category = defaultdict(float)
    transactions = db.session.query(Transaction.amount, Category.name, Transaction.transaction_type).join(
        Category, Transaction.category_id == Category.category_id
    ).filter(Transaction.transaction_type == 'expense').all()

    for amount, category_name, _ in transactions:
        spending_by_category[category_name] += amount

    income_vs_expense = {
        'income': total_income,
        'expense': total_expenses
    }

    spending_by_category = list(spending_by_category.items())  # Convert to list of tuples

    return render_template(
        'dashboard.html',
        total_income=total_income,
        total_expenses=total_expenses,
        remaining_balance=remaining_balance,
        recent_transactions=recent_transactions,
        spending_by_category=spending_by_category,  # Pass the list of tuples
        income_vs_expense=income_vs_expense
    )
