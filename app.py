from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Ruta del archivo JSON
USUARIOS_JSON = 'usuarios.json'

# Función para cargar usuarios desde el archivo JSON
def cargar_usuarios():
    if os.path.exists(USUARIOS_JSON):
        with open(USUARIOS_JSON, 'r') as file:
            return json.load(file)
    return []

# Función para guardar usuarios en el archivo JSON
def guardar_usuarios(usuarios):
    with open(USUARIOS_JSON, 'w') as file:
        json.dump(usuarios, file)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    usuarios = cargar_usuarios()

    # Verificar si el usuario ya existe
    for usuario in usuarios:
        if usuario['username'] == username:
            return "El usuario ya existe."

    # Agregar nuevo usuario
    usuarios.append({'username': username, 'password': password, 'email': email})
    guardar_usuarios(usuarios)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuarios = cargar_usuarios()

        # Verificar credenciales
        for usuario in usuarios:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                return redirect(url_for('profile'))

        return "Credenciales incorrectas."

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
