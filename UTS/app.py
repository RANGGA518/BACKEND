from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "kunci_rahasia_minimarket"

# --- KONFIGURASI DATABASE ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'harfandi123'
app.config['MYSQL_DB'] = 'db_minimarket'

mysql = MySQL(app)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================================================
#                ROUTE: HALAMAN UTAMA + PENCARIAN
# ============================================================
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    keyword = request.args.get('keyword', '').strip()

    cur = mysql.connection.cursor()
    parts = keyword.split()

    cur = mysql.connection.cursor()

    if len(parts) == 2 and parts[1].isdigit():
        # Keyword gabungan: nama + stok
        nama_kw, stok_kw = parts[0], parts[1]
        query_count = "SELECT COUNT(*) FROM barang WHERE nama LIKE %s AND stok = %s"
        query_data = "SELECT * FROM barang WHERE nama LIKE %s AND stok = %s LIMIT %s OFFSET %s"
        cur.execute(query_count, (f"%{nama_kw}%", stok_kw))
        total_data = cur.fetchone()[0]

        offset = (page - 1) * per_page
        cur.execute(query_data, (f"%{nama_kw}%", stok_kw, per_page, offset))

    elif keyword.isdigit():
        # Keyword angka tunggal  cocokkan ID atau stok
        query_count = "SELECT COUNT(*) FROM barang WHERE id = %s OR stok = %s"
        query_data = "SELECT * FROM barang WHERE id = %s OR stok = %s LIMIT %s OFFSET %s"
        cur.execute(query_count, (keyword, keyword))
        total_data = cur.fetchone()[0]

        offset = (page - 1) * per_page
        cur.execute(query_data, (keyword, keyword, per_page, offset))

    else:
        # Keyword kata → cocokkan nama saja
        query_count = "SELECT COUNT(*) FROM barang WHERE nama LIKE %s"
        query_data = "SELECT * FROM barang WHERE nama LIKE %s LIMIT %s OFFSET %s"
        cur.execute(query_count, (f"%{keyword}%",))
        total_data = cur.fetchone()[0]

        offset = (page - 1) * per_page
        cur.execute(query_data, (f"%{keyword}%", per_page, offset))

    data = cur.fetchall()
    total_pages = (total_data + per_page - 1) // per_page
    cur.close()

    return render_template('index.html', barang=data, page=page, total_pages=total_pages, keyword=keyword)

# ============================================================
#                ROUTE: TAMBAH BARANG
# ============================================================
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_barang():
    if request.method == 'POST':
        id = request.form['id_brg']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        gambar = request.files['gambar']

        filename = None
        if gambar and allowed_file(gambar.filename):
            filename = secure_filename(gambar.filename)
            gambar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO barang (id, nama, harga, stok, gambar) VALUES (%s, %s, %s, %s, %s)",
                        (id, nama, harga, stok, filename))
            mysql.connection.commit()
            flash("Barang berhasil ditambahkan!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash("Gagal menambah barang: " + str(e), "danger")
        finally:
            cur.close()

    return render_template('tambah.html')


# ============================================================
#                ROUTE: EDIT BARANG
# ============================================================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_barang(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        id_brg = request.form['id_brg']
        nama = request.form['nama']
        harga = request.form['harga']
        stok = request.form['stok']
        gambar_baru = request.files['gambar']

        cur.execute("SELECT gambar FROM barang WHERE id=%s", (id,))
        data_lama = cur.fetchone()
        gambar_lama = data_lama[0] if data_lama else None

        filename = gambar_lama  

        # Jika user upload gambar baru
        if gambar_baru and allowed_file(gambar_baru.filename):
            filename = secure_filename(gambar_baru.filename)
            gambar_baru.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if gambar_lama and gambar_lama != filename:
                path_lama = os.path.join(app.config['UPLOAD_FOLDER'], gambar_lama)
                if os.path.exists(path_lama):
                    os.remove(path_lama)


        try:
            cur.execute("UPDATE barang SET nama=%s, harga=%s, stok=%s, gambar=%s WHERE id=%s",
                        (nama, harga, stok, filename, id_brg))
            mysql.connection.commit()
            flash("Barang berhasil diperbarui!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash("Gagal mengupdate barang: " + str(e), "danger")
        finally:
            cur.close()
    else:
        cur.execute("SELECT * FROM barang WHERE id=%s", (id,))
        data = cur.fetchone()
        cur.close()
        if not data:
            flash("Barang tidak ditemukan!", "danger")
            return redirect(url_for('index'))
        return render_template('edit.html', barang=data)


# ============================================================
#                ROUTE: HAPUS BARANG
# ============================================================
@app.route('/hapus/<int:id>')
def hapus_barang(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM barang WHERE id=%s", (id,))
        mysql.connection.commit()
        flash("Barang berhasil dihapus!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash("Gagal menghapus barang: " + str(e), "danger")
    finally:
        cur.close()
    return redirect(url_for('index'))

# ============================================================
#                ROUTE: PENJUALAN
# ============================================================
@app.route('/penjualan', methods=['GET', 'POST'])
def penjualan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM barang")
    barang_list = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        id_barang = request.form['id_barang']
        jumlah = int(request.form['jumlah'])

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM barang WHERE id = %s", (id_barang,))
        barang = cur.fetchone()

        if not barang:
            flash("Barang tidak ditemukan!", "danger")
            return redirect(url_for('penjualan'))

        if jumlah > barang[3]:
            flash("Stok tidak mencukupi!", "danger")
            return redirect(url_for('penjualan'))

        subtotal = barang[2] * jumlah

        # Update stok barang
        cur.execute("UPDATE barang SET stok = stok - %s WHERE id = %s", (jumlah, id_barang))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('transaksi_selesai', nama=barang[1], harga=barang[2], jumlah=jumlah, subtotal=subtotal))

    return render_template('penjualan.html', barang_list=barang_list)


# ============================================================
#                ROUTE: TRANSAKSI SELESAI
# ============================================================
@app.route('/transaksi_selesai')
def transaksi_selesai():
    nama = request.args.get('nama')
    harga = float(request.args.get('harga'))
    jumlah = int(request.args.get('jumlah'))
    subtotal = float(request.args.get('subtotal'))

    return render_template('transaksi_selesai.html',
                           nama=nama,
                           harga=harga,
                           jumlah=jumlah,
                           subtotal=subtotal)



# ============================================================
#                JALANKAN APLIKASI
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)
