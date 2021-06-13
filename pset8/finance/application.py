import os
import sys

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash_rows = db.execute("SELECT cash FROM users WHERE id=:id", id = session["user_id"])
    cash_left = round(float(cash_rows[0]["cash"]),2)
    transaction_rows = db.execute("SELECT * FROM transactions WHERE id=:id", id = session["user_id"])
    total = db.execute("SELECT SUM(total) AS total FROM transactions WHERE id=:id", id = session["user_id"])[0]["total"]

    if total is None:
        total = 0
    total_cash = round((total + cash_left), 2)

    return render_template("index.html", transaction_rows=transaction_rows, cash_left=cash_left, total_cash=total_cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Check for errors
        if not request.form.get("symbol"):
            return apology("You must provide the stock symbol.", 400)
        elif not request.form.get("shares").isdigit():
            return apology("You must digit how many shares you want to buy.", 400)

        # Get what user inputed and analyse the stock requested
        symbols = request.form.get("symbol").upper()
        stock = lookup(symbols)
        bought_shares = int(request.form.get("shares"))
        buyPrice = round(stock["price"], 2)
        total_buy = round(buyPrice * bought_shares, 2)
        # Check if the stock exists
        if stock == None:
            return apology("Stock not found", 400)

        # Get the user cash in the table
        rows = db.execute("SELECT cash FROM users WHERE id = :id",
                            id = session["user_id"])
        # See if the user can afford the stock
        cash = round(float(rows[0]["cash"]),2)

        if cash < total_buy:
            return apology("You don't have enough money.", 400)
        # If he can, update cash value
        update_cash = round((cash - (buyPrice * bought_shares)), 2)
        # Check if the user have cash avaiable to afford other stock
        if update_cash <= 0:
            return apology("You are out of money.")

        # Updates the user cash in the table
        db.execute("UPDATE users SET cash = :updated_cash WHERE id = :id",
                    updated_cash = update_cash,
                    id = session["user_id"])

        # Insert into history table the buy transaction
        db.execute("INSERT INTO history (id, symbol, type, shares, price, total) VALUES (:id, :symbol, :type, :shares, :price, :total)",
                    id=session["user_id"],
                    symbol=symbols,
                    type="Buy",
                    shares=bought_shares,
                    price=buyPrice,
                    total= total_buy)


        # Updates the transactions table
        rows = db.execute("SELECT * FROM transactions WHERE id=:id AND symbol=:symbol",
                                id=session["user_id"],
                                symbol=symbols)
        # If there are no shares of the symbol, insert a new row in transactions
        if len(rows) == 0:
            db.execute("INSERT INTO transactions (id, symbol, shares, buy_price, name, total) VALUES (:id, :symbol, :shares, :buyPrice, :name, :total)",
                        id=session["user_id"],
                        symbol=symbols,
                        shares=bought_shares,
                        buyPrice=buyPrice,
                        name=stock["name"],
                        total= total_buy)
        else:
            db.execute("UPDATE transactions SET shares = (shares + :shares), buy_price=:buyPrice, bought_shares = shares + :bought_shares total = (total + :total) WHERE id=:id",
                        id=session["user_id"],
                        shares=bought_shares,
                        bought_shares=bought_shares,
                        total= total_buy,
                        buyPrice=buyPrice)
        # Redirect user to the homepage after buying
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_rows = db.execute("SELECT * FROM history WHERE id=:id", id=session["user_id"])
    return render_template("history.html", history_rows=history_rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        if not request.form.get("quote"):
            return apology("You must provide the stock symbol.", 400)

        symbol = request.form.get("quote").upper()
        stock = lookup(symbol)

        if stock == None:
            return apology("Stock not found", 400)

        #Print the quote for the user
        return render_template("quoted.html", stock=stock)

    # Open the quote route to the user
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the user provided a username
        if not request.form.get("username"):
            return apology("You must provide a username.", 403)

        # Check if the user provided a password
        elif not request.form.get("password"):
            return apology("You must provide a passoword", 403)

        # Check if the user confirmed his/her password
        elif not request.form.get("confirmation"):
            return apology("You must confirm your passoword", 403)

        # Check if the user passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Your confirmed password needs to match with your passowrd", 403)



        # Check if username already exist
        while True:
            try:
                insert = db.execute("INSERT INTO users (username, hash) VALUES (:username, :password_hash)",
                          username = request.form.get("username"),
                          password_hash = generate_password_hash(request.form.get("password")))
                break
            except:
                return apology("Failed to register: username already exist.", 403)

        # Set session id to the new user id
        session["user_id"] = insert

        # Redirect user to homepage
        return redirect("/")

    # Open the register form to the user
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Get what the user inputed
        sold_shares = int(request.form.get("shares"))
        if not request.form.get("shares").isdigit():
            return apology("You must digit how many shares you want to sell.", 400)

        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        ownedShares = db.execute("SELECT shares, symbol FROM transactions WHERE id=:id AND symbol=:symbol",
                                    id = session["user_id"],
                                    symbol=symbol)
        symbol_shares = ownedShares[0]["shares"]
        # Get sell price
        sellPrice = round(stock["price"], 2)
        # Get total sell price
        total_sell = round(sellPrice * sold_shares, 2)
        # Update total
        total = db.execute("SELECT total FROM transactions WHERE id=:id AND symbol=:symbol",
                                    id = session["user_id"],
                                    symbol=symbol)[0]["total"]
        update_total = round(total - total_sell, 2)

        # Check if the user has enough shares to sell
        if sold_shares > symbol_shares:
            return apology("You don't have enough shares to sell.", 403)
        else:
            # Get the user cash in the table
            rows = db.execute("SELECT cash FROM users WHERE id = :id",
                            id = session["user_id"])
            cash = rows[0]["cash"]
            update_cash = round((cash + (sellPrice * sold_shares)), 2)


            # Updates the user cash in the table
            db.execute("UPDATE users SET cash = :updated_cash WHERE id = :id",
                                            id = session["user_id"],
                                            updated_cash = update_cash)
            # Updates the user shares of the symbol sold in the table
            db.execute("UPDATE transactions SET shares = (shares - :shares), sold_shares = (shares + :sold_shares), total = :total, sell_price=:sellPrice WHERE id=:id AND symbol=:symbol",
                                                shares=sold_shares,
                                                sold_shares=sold_shares,
                                                id = session["user_id"],
                                                symbol = symbol,
                                                total = update_total,
                                                sellPrice = sellPrice)

             # Insert into history table the sell transaction
            db.execute("INSERT INTO history (id, symbol, type, shares, price, total) VALUES (:id, :symbol, :type, :shares, :price, :total)",
                    id=session["user_id"],
                    symbol=symbol,
                    type="Sell",
                    shares=sold_shares * -1,
                    price=sellPrice,
                    total=total_sell)

            # Delete rows that don't have any share when sold
            db.execute("DELETE FROM transactions WHERE id=:id AND shares=:shares AND symbol=:symbol",
                        id = session["user_id"],
                        shares = 0,
                        symbol = symbol)

        return redirect("/")
    else:
        symbol_rows = db.execute("SELECT symbol FROM transactions WHERE id=:id",
                                id = session["user_id"])

        return render_template("sell.html", symbol_rows=symbol_rows)

@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "POST":
        added_cash = float(request.form.get("cash"))
        cash = float(db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])[0]["cash"])
        total_cash = round((cash + added_cash),2)

        # Let the user just add 1 to 10000 cash inclusive
        if  added_cash < 1 or added_cash > 10000:
            return apology("You can just add cash from 1 to 10000 inclusive.")

        # Update cash in table
        db.execute("UPDATE users SET cash = :cash WHERE id=:id",
                    cash=total_cash,
                    id=session["user_id"])
        # Insert into history table the add cash transaction
        db.execute("INSERT INTO history (id, symbol, type, shares, price, total) VALUES (:id, :symbol, :type, :shares, :price, :total)",
        id=session["user_id"],
        symbol="CASH",
        type="Addcash",
        shares= 1,
        price=added_cash,
        total=added_cash)
        return redirect("/")
    else:
        return render_template("addcash.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
