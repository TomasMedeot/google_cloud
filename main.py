from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

def conectar_db():
    return sqlite3.connect('usuarios.db')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if verificar_credenciales(usuario, contraseña):
            session['usuario'] = usuario
            return redirect(url_for('pagina_restringida'))
        else:
            return render_template('login.html', mensaje="Credenciales incorrectas")
    return render_template('login.html', mensaje="")

def verificar_credenciales(usuario, contraseña):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contraseña=?", (usuario, contraseña))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

@app.route('/user')
def pagina_restringida():
    if 'usuario' in session:
        return render_template('user.html', usuario=session['usuario'])
    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if not usuario or not contraseña:
            return render_template('register.html', mensaje="Por favor, completa todos los campos.")
        if usuario_existe(usuario):
            return render_template('register.html', mensaje="El usuario ya existe. Por favor, elige otro.")
        registrar_usuario(usuario, contraseña)
        return redirect(url_for('login'))
    return render_template('register.html', mensaje="")

def usuario_existe(usuario):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

def registrar_usuario(usuario, contraseña):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña))
    conexion.commit()
    conexion.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
