from flask import Flask, request, redirect, jsonify
import sqlite3
import qrcode
import os

app = Flask(__name__)

# Database Setup
def init_db():
    conn = sqlite3.connect('suggestions.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS suggestions (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      suggestion TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Home Page (Suggestion Form)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        suggestion = request.form['suggestion']
        conn = sqlite3.connect('suggestions.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO suggestions (suggestion) VALUES (?)", (suggestion,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Thank you for your suggestion!"})
    return jsonify({"message": "Submit your suggestion using a POST request."})

# View Suggestions
@app.route('/view')
def view_suggestions():
    conn = sqlite3.connect('suggestions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suggestions")
    data = cursor.fetchall()
    conn.close()
    return jsonify({"suggestions": data})

# Generate QR Code
def generate_qr():
    url = "https://yourapp.onrender.com"  # Replace with actual URL after deployment
    qr = qrcode.make(url)
    if not os.path.exists("static"):
        os.makedirs("static")
    qr.save("static/qr_code.png")

generate_qr()

if __name__ == '__main__':
    app.run(debug=True)
