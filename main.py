from flask import Flask, render_template, request, redirect, url_for, session
from usuarios import verificar_credenciales, usuario_existe, registrar_usuario

app = Flask(__name__)
app.secret_key = 'clave_codex123'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['email']
        contraseña = request.form['contraseña']

        if verificar_credenciales(usuario, contraseña):
            session['usuario'] = usuario
            return redirect(url_for('pagina_restringida'))
        
        else:
            return render_template('login.html', mensaje="Credenciales incorrectas")
        
    return render_template('login.html', mensaje="")

@app.route('/user')
def pagina_restringida():
    if 'usuario' in session:
        return render_template('user.html', usuario=session['usuario'])
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['email']
        contraseña = request.form['contraseña']
        nombre = request.form['nombre']
        telefono = int(request.form['telefono'])

        if usuario_existe(usuario):
            return render_template('register.html', mensaje="El usuario ya existe. Por favor, elige otro.")
        
        registrar_usuario(usuario, contraseña, nombre, telefono)
        return redirect(url_for('login'))
    
    return render_template('register.html', mensaje="")

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='localhost', port=5000, debug=True)