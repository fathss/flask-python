from flask import Flask, session, flash, render_template, request, redirect, url_for
from models import db, Mahasiswa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mahasiswa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kuncirahasia'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Cek apakah user sudah login
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.')
        return redirect('/login')

    mahasiswa = Mahasiswa.query.all() # Mengambil semua data dari tabel Mahasiswa
    return render_template('index.html', mahasiswa=mahasiswa)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        from models import User
        username = request.form['username']
        password = request.form['password']
        
        # Cek apakah username sudah terdaftar
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar.')
            return redirect('/register')
        
        user = User(username=username) # Intantiate object bernama user dari class User
        user.set_password(password) # Menggunakan method set_password dari class User
        
        db.session.add(user)
        db.session.commit()
        flash('Pendaftaran berhasil. Silakan login.')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from models import User
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password): # Cek apakah username dan password sama
            session['user_id'] = user.id
            flash('Login berhasil.')
            return redirect('/')
        else:
            flash('Username atau password salah.')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Anda telah logout.')
    return redirect('/login')

@app.route('/tambah', methods=['POST'])
def tambah():
    if 'user_id' not in session:
        return redirect('/login')

    nama = request.form['nama']
    mhs = Mahasiswa(nama=nama) # Instantiate object bernama mhs dari class Mahasiswa
    db.session.add(mhs)
    db.session.commit()
    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    mhs = Mahasiswa.query.get_or_404(id)
    if request.method == 'POST':
        mhs.nama = request.form['nama']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', mhs=mhs)

@app.route('/hapus/<int:id>')
def hapus(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    target = Mahasiswa.query.get_or_404(id)
    db.session.delete(target)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)