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
    # Obtener datos del formulario
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Validar si el usuario ya existe
    usuarios = cargar_usuarios()
    for usuario in usuarios:
        if usuario['username'] == username:
            return "El usuario ya existe.", 400  # Código de error 400

    # Validar que los campos no estén vacíos
    if not username or not password or not email:
        return "Todos los campos son obligatorios.", 400

    # Agregar el nuevo usuario
    usuarios.append({'username': username, 'password': password, 'email': email})
    guardar_usuarios(usuarios)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cargar usuarios y verificar las credenciales
        usuarios = cargar_usuarios()
        for usuario in usuarios:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                return redirect(url_for('profile'))

        return "Credenciales incorrectas.", 401  # Código de error 401

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

# Asegúrate de que la aplicación se ejecute correctamente en producción
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Usa esto solo para desarrollo local, en Render usaremos Gunicorn
