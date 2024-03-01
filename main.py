from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Clave secreta para sesiones

# Función para conectarse a la base de datos SQLite
def conectar_db():
    return sqlite3.connect('usuarios.db')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if verificar_credenciales(usuario, contraseña):
            # Si las credenciales son correctas, establece una sesión y redirige a la página restringida
            session['usuario'] = usuario
            return redirect(url_for('pagina_restringida'))
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            return render_template('login.html', mensaje="Credenciales incorrectas")
    # Si es una solicitud GET o las credenciales son incorrectas, muestra el formulario de inicio de sesión
    return render_template('login.html', mensaje="")

# Función para verificar las credenciales del usuario en la base de datos SQLite
def verificar_credenciales(usuario, contraseña):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contraseña=?", (usuario, contraseña))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

# Ruta restringida
@app.route('/restringido')
def pagina_restringida():
    if 'usuario' in session:
        return render_template('restringido.html', usuario=session['usuario'])
    else:
        # Si no hay sesión de usuario, redirige al inicio de sesión
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
def logout():
    # Elimina la sesión de usuario y redirige al inicio de sesión
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if not usuario or not contraseña:
            return render_template('registro.html', mensaje="Por favor, completa todos los campos.")
        if usuario_existe(usuario):
            return render_template('registro.html', mensaje="El usuario ya existe. Por favor, elige otro.")
        registrar_usuario(usuario, contraseña)
        return redirect(url_for('login'))
    return render_template('registro.html', mensaje="")

# Función para verificar si un usuario ya existe en la base de datos SQLite
def usuario_existe(usuario):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

# Función para registrar un nuevo usuario en la base de datos SQLite
def registrar_usuario(usuario, contraseña):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña))
    conexion.commit()
    conexion.close()

if __name__ == '__main__':
   # print(pymysql.connect(host='localhost',user='root',password='password',db='test'))
    app.run(host='0.0.0.0', port=5000)
