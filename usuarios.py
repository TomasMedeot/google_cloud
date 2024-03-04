import sqlite3

def conectar_db():
    return sqlite3.connect('usuarios.sqlite3')

def usuario_existe(email):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE EMAIL=?", (email,))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None

def registrar_usuario(email, contraseña, nombre, telefono):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO usuarios (email, contraseña, nombre, telefono) VALUES (?, ?, ?, ?)", (email, contraseña, nombre, telefono))
    conexion.commit()
    conexion.close()

def verificar_credenciales(usuario, contraseña):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND contraseña=?", (usuario, contraseña))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado is not None