import sqlite3 as sql
import random
from datetime import datetime as dt
from flask import Flask, render_template, request, redirect, url_for

DATABASE_PATH = "expense_calc.db"

app = Flask(__name__, template_folder="")


def query_run(statement, flag=False):
    out = []
    try:
        conn = sql.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(statement)
        if flag:
            conn.commit()
        out = cursor.fetchall()
        conn.close()
    except Exception as err:
        print("Database operation failed: ", err)
    return out


def calc_avg():
    balance = 0
    min_date = "SELECT MIN(Date) FROM EXPENSE;"
    out = query_run(min_date)

    if len(out) > 0 and out[0][0] is not None:
        min_date = dt.strptime(out[0][0], '%Y-%m-%d')
    else:
        # Set min_date to today's date if no records exist
        min_date = dt.today()

    curr_date = dt.today()
    days_diff = (curr_date - min_date).days + 1

    earned_query = "SELECT SUM(Amount) FROM EXPENSE WHERE Type='Credit';"
    spent_query = "SELECT SUM(Amount) FROM EXPENSE WHERE Type='Debit';"

    out1 = query_run(earned_query)
    out2 = query_run(spent_query)

    if len(out1) > 0 and type(out1[0][0]) == float:
        balance = out1[0][0]

    if len(out2) > 0 and type(out2[0][0]) == float:
        balance -= out2[0][0]

    daily_avg = balance / days_diff
    return dt.strftime(min_date, '%Y-%m-%d'), balance, daily_avg


@app.route("/")
def expense_read():
    read_query = "SELECT * FROM EXPENSE;"
    expense_list = query_run(read_query)
    min_date, balance, avg = calc_avg()
    msg = "".join(["Your total balance is Rs: ", str(balance),
                   " and daily average is Rs: ", str(round(avg, 3)),
                   " since ", min_date])
    return render_template("index.html", exp_list=expense_list, message=msg)


@app.route("/create", methods=['POST'])
def expense_write():
    if request.method == 'POST':
        query_mod = "SELECT MAX(ID) FROM EXPENSE_CALC;"
        out = query_run(query_mod)
        if len(out) > 0:
            if type(out[0][0]) == int:
                exp_id = out[0][0] + 1
            else:
                exp_id = 1
        else:
            exp_id = random.randint(1000, 100000)
        write_query = "INSERT INTO EXPENSE " \
                      "(ID, DESCRIPTION, TYPE, DATE, AMOUNT) VALUES"
        write = "".join([write_query, "(", str(exp_id), ",'",
                         request.form['Description'], "', '",
                         request.form['Type'], "', '",
                         request.form['Date'], "',", str(request.form['Amount']), " );"])
        query_run(write, True)

    return redirect(url_for("expense_read"))


@app.route("/delete/<exp_id>", methods=["POST"])
def expense_remove(exp_id):
    if request.method == "POST":
        delete = "DELETE FROM EXPENSE WHERE ID="
        delete_query = "".join([delete, str(exp_id), ";"])
        query_run(delete_query, True)

    return redirect(url_for("expense_read"))


@app.route("/update/<exp_id>", methods=["POST"])
def expense_update(exp_id):
    if request.method == "POST":
        update_query = "UPDATE EXPENSE SET "
        update = "".join([update_query, "Description='",
                          request.form['Description'], "', Type='",
                          request.form['Type'], "', Date='",
                          request.form['Date'], "', Amount=",
                          str(request.form['Amount']), " WHERE ID=",
                          str(exp_id), ";"])
        query_run(update, True)

    return redirect(url_for("expense_read"))


def create_expense_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS EXPENSE (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DESCRIPTION TEXT NOT NULL,
        TYPE TEXT CHECK(TYPE IN ('Credit', 'Debit')) NOT NULL,
        DATE TEXT NOT NULL,
        AMOUNT REAL NOT NULL
    );
    """
    query_run(create_table_query, True)


if __name__ == "__main__":
    create_expense_table()
    app.run(debug=True, port=9000)
