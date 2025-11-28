from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
Bootstrap(app)

# koneksi ke MONGO
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["db_minimarket"]
collection = db["barang"]

# route untuk menampilkan semua data
@app.route('/')
def index() :
    items = collection.find()
    return render_template("index.html", items=items)

# route untuk menambah data baru
@app.route('/add', methods=['GET', 'POST'])
def add() :
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        collection.insert_one({'kode' : kode, 'nama' : nama, 'harga' : harga, 'stok' : stok})
        return redirect(url_for('index'))
    return render_template('add.html')

# route untuk edit
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id) :
    items = collection.find_one({'_id' : ObjectId(id)})

    if request.method == 'POST':
        kode = request.form['kode'] 
        nama = request.form['nama'] 
        harga = request.form['harga'] 
        stok = request.form['stok'] 

        collection.update_one({'_id': ObjectId(id)}, {'$set': {'kode' : kode, 'nama' : nama, 'harga' : harga, 'stok' : stok}})
        return redirect(url_for('index'))
    return render_template('edit.html', items=items)

# route hapus
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id) :
    collection.delete_one({'_id' : ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug=True)