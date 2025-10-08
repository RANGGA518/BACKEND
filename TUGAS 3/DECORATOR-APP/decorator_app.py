from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Dekorator before_request ---
@app.before_request
def before():
    print("Sebelum request dijalankan")

# --- Routing utama ---
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '123':
        return redirect(url_for('dashboard'))
    else:
        return "Login gagal! Username atau password salah."

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# --- Dekorator after_request ---
@app.after_request
def after(response):
    print("Setelah request selesai dieksekusi")
    return response

# --- Dekorator teardown_request ---
@app.teardown_request
def teardown(exception=None):
    print("Request selesai, resources dibersihkan")

if __name__ == '__main__':
    app.run(debug=True)
