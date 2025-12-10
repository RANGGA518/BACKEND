from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# koneksi database
def db():
    conn = sqlite3.connect("stokumkm.db")
    conn.row_factory = sqlite3.Row
    return conn

# Buat Table
def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS barang(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                 kode CHAR NOT NULL,
                 nama VARCHAR NOT NULL,
                 harga INT NOT NULL,
                 jumlah INT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()
# Read
@app.route("/")
def index():
    conn = db()
    rows = conn.execute("SELECT * FROM barang").fetchall()
    conn.close()
    return render_template("index.html", stoks=rows)

# Create
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        conn = db()
        conn.execute("INSERT INTO barang (kode, nama, harga, jumlah) Values (?, ?, ?, ?)", (kode, nama, harga, jumlah))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# Update
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = db()
    stok = conn.execute("SELECT * FROM barang WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        kode = request.form["kode"]
        nama = request.form["nama"]
        harga = request.form["harga"]
        jumlah = request.form["jumlah"]
        conn.execute("UPDATE barang SET kode=?, nama=?, harga=?, jumlah=? WHERE id=?", (kode, nama, harga, jumlah, id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    
    conn.close()
    return render_template("edit.html", stoks=stok)

# Delete
@app.route("/delete/<int:id>")
def delete(id):
    conn = db()
    conn.execute("DELETE FROM barang WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)