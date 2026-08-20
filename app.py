import sqlite3
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_super_secreta_petshop')

DB_NAME = 'petshop.db'

# --- FUNCIÓN DE CONEXIÓN A SQLITE ---
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- INICIALIZACIÓN AUTOMÁTICA DE TABLAS ---
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT,
            nombre TEXT,
            apellido TEXT,
            telefono TEXT,
            email TEXT UNIQUE,
            password TEXT,
            tipo_usuario INTEGER DEFAULT 0
        )
    ''')

    # Tabla Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            descripcion TEXT,
            img TEXT,
            categoria TEXT
        )
    ''')

    # Tabla Consejos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consejos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            texto TEXT
        )
    ''')

    # Crear administrador por defecto si no existe
    cursor.execute("SELECT * FROM clientes WHERE email = 'admin@petshop.com'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO clientes (dni, nombre, apellido, telefono, email, password, tipo_usuario)
            VALUES ('11111111', 'Admin', 'General', '12345678', 'admin@petshop.com', 'admin123', 1)
        ''')

    # Cargar datos iniciales de consejos si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM consejos")
    if cursor.fetchone()[0] == 0:
        consejos_iniciales = [
            ("¿Cómo cuidar a tu mascota?", "Dejale agua disponible siempre."),
            ("12 cosas que no debes hacer", "No utilices tus manos o pies para jugar."),
            ("Tips para cuidar a tu perro", "Acaricia a tu perro: un trato amoroso."),
            ("¿Cómo me acerco a un perro?", "Pedí permiso a sus dueños."),
            ("Tu gato necesita ciertos cuidados", "Protección en las ventanas.")
        ]
        cursor.executemany("INSERT INTO consejos (titulo, texto) VALUES (?, ?)", consejos_iniciales)

    conn.commit()
    conn.close()

init_db()


# --- DECORADOR PARA RUTAS ADMIN ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or session.get('tipo_usuario') != 1:
            flash('Acceso denegado: Se requieren permisos de administrador.')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


# --- RUTAS PÚBLICAS Y AUTENTICACIÓN ---
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM clientes WHERE email = ? AND password = ?", (email, password)).fetchone()
        conn.close()
        
        if user:
            session['logged_in'] = True
            session['email'] = user['email']
            session['tipo_usuario'] = int(user['tipo_usuario'])
            
            if session['tipo_usuario'] == 0:
                flash("Acceso Correcto!")
                return render_template('home.html')
            elif session['tipo_usuario'] == 1:
                flash("Acceso Correcto a las funciones de Administrador.")
                return render_template('admin.html')
        else:
            flash("Error de acceso. Credenciales incorrectas.")
            return render_template('login.html')
            
    return render_template('login.html')

@app.route('/registro', methods=["GET", "POST"])
def registro():
    if request.method == 'GET':
        return render_template("registro.html")
    else:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO clientes(dni, nombre, apellido, telefono, email, password, tipo_usuario) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (request.form['dni'], request.form['nombre'], request.form['apellido'], 
              request.form['telefono'], request.form['email'], request.form['password'], 0))
        conn.commit()
        conn.close()
        flash("Registro exitoso. Por favor inicia sesión.")
        return redirect(url_for('login'))

@app.route('/salir', methods=["GET", "POST"])
def salir():
    session.clear()
    return render_template("home.html")


# --- RUTAS PROTEGIDAS (ADMIN) ---
@app.route('/admin', methods=['GET'])
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/listado', methods=['GET'])
@admin_required
def listar():
    conn = get_db_connection()
    clientes = conn.execute("SELECT * FROM clientes").fetchall()
    conn.close()
    return render_template('listado.html', clientes=clientes)

@app.route('/actualizar/<id>', methods=['POST','GET'])
@admin_required
def actualizar(id):
    conn = get_db_connection()
    if request.method == 'POST':
        conn.execute('''
            UPDATE clientes SET dni = ?, nombre = ?, apellido = ?, telefono = ?, 
            email = ?, password = ?, tipo_usuario = ? WHERE id = ?
        ''', (request.form['dni'], request.form['nombre'], request.form['apellido'], 
              request.form['telefono'], request.form['email'], request.form['password'], 
              request.form['tipo_usuario'], id))
        conn.commit()
        conn.close()
        flash('Registro actualizado.')
        return redirect(url_for('listar'))
    
    cliente = conn.execute("SELECT * FROM clientes WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('editar.html', clientes=cliente)

@app.route('/eliminar/<string:id>')
@admin_required
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Contacto removido correctamente.')
    return redirect(url_for('listar'))

@app.route('/agregarProd', methods=['POST', 'GET'])
@admin_required
def agregarProd():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO productos (nombre, precio, descripcion, img, categoria) 
            VALUES (?, ?, ?, ?, ?)
        ''', (request.form['nombre'], request.form['precio'], request.form['descripcion'], 
              request.form['img'], request.form['categoria']))
        conn.commit()
        conn.close()
        flash('Producto agregado correctamente!')
    return render_template('agregar.html')

@app.route('/productos/<string:id>') 
@admin_required
def eliminarProd(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado correctamente.')
    return redirect(url_for('productos'))

@app.route('/productos', methods=['GET'])
@admin_required
def productos():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)


# --- RUTAS PÚBLICAS DE CATÁLOGO ---
@app.route('/gatos')
def listarG():    
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos WHERE categoria = 'Gatos'").fetchall()
    conn.close()
    return render_template('gatos.html', productos=productos)

@app.route('/perros')
def listarP():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos WHERE categoria = 'Perros'").fetchall()
    conn.close()
    return render_template('perros.html', productos=productos)

@app.route('/otros')
def listarO():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos WHERE categoria = 'Otros'").fetchall()
    conn.close()
    return render_template('otros.html', productos=productos)


# --- SECCIÓN EXCLUSIVA (REQUIERE LOGIN) ---
@app.route('/consejos')
def consejo():
    if 'email' in session:
        conn = get_db_connection()
        consejos = conn.execute("SELECT * FROM consejos").fetchall()
        conn.close()
        return render_template('consejos.html', consejo=consejos)
    
    flash('Debes iniciar sesión o registrarte para acceder a la sección de consejos.')
    return redirect(url_for('login'))

@app.route('/consejos/<id>')
def contenido(id):
    if 'email' in session:
        conn = get_db_connection()
        consejo = conn.execute("SELECT * FROM consejos WHERE id = ?", (id,)).fetchall()
        conn.close()
        return render_template('consejos_contenido.html', consejo=consejo)
    
    flash('Debes iniciar sesión o registrarte para acceder a esta sección.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)