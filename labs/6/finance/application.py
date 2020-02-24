import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query database for user's cash
    rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    if not rows:
        return apology("missing user")
    cash = rows[0]["cash"]
    total = cash

    # Query database for user's stocks
    stocks = db.execute("""SELECT symbol, SUM(shares) AS shares FROM transactions
        WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0""", user_id=session["user_id"])

    # Query Yahoo for stocks' latest names and prices
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        total += stock["shares"] * quote["price"]

    # Render portfolio
    return render_template("index.html", cash=cash, stocks=stocks, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Enable user to buy a stock."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")
        elif not request.form.get("shares"):
            return apology("missing shares")
        elif not request.form.get("shares").isdigit():
            return apology("invalid shares")
        shares = int(request.form.get("shares"))
        if not shares:
            return apology("too few shares")

        # Get stock quote
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol")

        # Cost to buy
        cost = shares * quote["price"]

        # Get user's cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
        if not rows:
            return apology("missing user")
        cash = rows[0]["cash"]

        # Ensure user can afford
        if cash < cost:
            return apology("can't afford")

        # Record purchase
        db.execute("""INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES(:user_id, :symbol, :shares, :price)""",
                   user_id=session["user_id"], symbol=quote["symbol"], shares=shares, price=quote["price"])

        # Deduct cash
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id",
                   cost=cost, id=session["user_id"])

        # Display portfolio
        flash("Bought!")
        return redirect("/")

    # GET
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = :username", username=username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Display user's history of transactions."""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get a stock quote."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")

        # Get stock quote
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("invalid symbol")

        # Display quote
        return render_template("quoted.html", quote=quote)

    # GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user for an account."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match")

        # Add user to database
        id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(request.form.get("password")))
        if not id:
            return apology("username taken")

        # Log user in
        session["user_id"] = id

        # Let user know they're registered
        flash("Registered!")
        return redirect("/")

    # GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Enable user to sell a stock."""

    # POST
    if request.method == "POST":

        # Validate form submission
        if not request.form.get("symbol"):
            return apology("missing symbol")
        symbol = request.form.get("symbol").upper()
        if not request.form.get("shares"):
            return apology("missing shares")
        elif not request.form.get("shares").isdigit():
            return apology("invalid shares")
        shares = int(request.form.get("shares"))
        if shares < 1:
            return apology("shares must be positive")

        # Check how many shares user owes
        rows = db.execute("""SELECT SUM(shares) AS shares FROM transactions
            WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol""",
                          user_id=session["user_id"], symbol=symbol)
        if len(rows) != 1:
            return apology("symbol not owned")
        if shares > rows[0]["shares"]:
            return apology("too many shares")

        # Get stock quote
        quote = lookup(request.form.get("symbol"))

        # Record sale
        db.execute("""INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES(:user_id, :symbol, :shares, :price)""",
                   user_id=session["user_id"], symbol=quote["symbol"], shares=-shares, price=quote["price"])

        # Deposit cash
        db.execute("UPDATE users SET cash = cash + :value WHERE id = :id",
                   value=shares * quote["price"], id=session["user_id"])

        # Display portfolio
        flash("Sold!")
        return redirect("/")

    # GET
    else:

        # Get symbols owned
        rows = db.execute("""SELECT symbol FROM transactions
            WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0""",
            user_id=session["user_id"])
        symbols = [row["symbol"] for row in rows]

        # Display sales form
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
