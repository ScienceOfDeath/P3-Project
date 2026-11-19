from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            discount REAL,
            secret_note TEXT
        )
    ''')
    cursor.execute("DELETE FROM coupons")
    cursor.execute("INSERT INTO coupons (code, discount, secret_note) VALUES ('WINTER26', 25.0, 'Standard winter discount')")
    cursor.execute("INSERT INTO coupons (code, discount, secret_note) VALUES ('VIP50', 50.0, 'Exclusive VIP discount')")
    cursor.execute("INSERT INTO coupons (code, discount, secret_note) VALUES ('ADMIN100', 100.0, 'Admin discount')")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_code = request.form.get("code", "")
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # TODO: Query the database to get the code, discount, and secret_note for the given user_code
        
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            result = [(f"Error: {e}", "", "")]
            
        conn.close()
        
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)