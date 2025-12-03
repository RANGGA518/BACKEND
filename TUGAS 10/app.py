from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["db_minimarket"]
collection = db["barang"]

# INDEX
@app.route('/')
def index():
    data = list(collection.find())
    return render_template("index.html", data=data)

# ADD
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']

        # upload image
        file = request.files['gambar']
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        collection.insert_one({
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "stok": stok,
            "gambar": filename
        })

        return redirect(url_for('index'))
    
    return render_template('add.html')

# EDIT
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = collection.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']

        filename = item.get('gambar')

        # If user uploads a new file
        file = request.files['gambar']
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                "kode": kode,
                "nama": nama,
                "harga": harga,
                "stok": stok,
                "gambar": filename
            }}
        )

        return redirect(url_for('index'))

    return render_template('edit.html', item=item)

# DELETE
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
