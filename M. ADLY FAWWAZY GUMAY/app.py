from flask import Flask, render_template, request, redirect, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shoe_inventory"
)

cursor = db.cursor()

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stock')
def stock():
    cursor.execute("SELECT * FROM shoes")
    shoes = cursor.fetchall()
    return render_template('stock.html', shoes=shoes)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def index():
    cursor.execute("SELECT * FROM shoes")
    shoes = cursor.fetchall()
    return render_template('index.html', shoes=shoes)

@app.route('/add', methods=['GET', 'POST'])
def add_shoes():
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        stock = request.form['stock']

        if not name or not size or not stock:
            flash('Semua kolom harus diisi!', 'error')
            return redirect('/add')

        cursor.execute(
            "INSERT INTO shoes (name, size, stock) VALUES (%s, %s, %s)",
            (name, size, stock)
        )
        db.commit()
        flash('Sepatu berhasil ditambahkan!', 'success')
        return redirect('/')
    return render_template('add_shoes.html')



if __name__ == '__main__':
    app.run(debug=True)
