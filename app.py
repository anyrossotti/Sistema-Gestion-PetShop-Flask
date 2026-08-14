import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_por_defecto_si_no_hay_env')
mysql = MySQL(app)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))

# --- RUTAS PÚBLICAS ---
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        if user:
            session['logged_in'] = True
            session['email'] = user[5]
            session['tipo_usuario'] = int(user[7]) 
            
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
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clientes(dni, nombre, apellido, telefono, email, password, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (request.form['dni'], request.form['nombre'], request.form['apellido'], request.form['telefono'], request.form['email'], request.form['password'], 0))
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route('/salir', methods=["GET", "POST"])
def salir():
    session.clear()
    return render_template("home.html")

# --- RUTAS PROTEGIDAS (ADMIN) ---
@app.route('/admin', methods=['GET'])
def admin():
    if 'email' in session and session.get('tipo_usuario') == 1:
        return render_template('admin.html')
    flash('Acceso denegado: Solo administradores.')
    return render_template("home.html")

@app.route('/listado', methods=['GET'])
def listar():
    if 'email' in session and session.get('tipo_usuario') == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        return render_template('listado.html', clientes=cur.fetchall())
    flash('Acceso denegado.')
    return render_template("home.html")

@app.route('/actualizar/<id>', methods=['POST','GET'])
def actualizar(id):
    if 'email' in session and session.get('tipo_usuario') == 1:
        if request.method == 'POST':
            cur = mysql.connection.cursor()  
            cur.execute("""UPDATE clientes SET dni = %s, nombre = %s, apellido = %s, telefono = %s, 
            email = %s, password = %s, tipo_usuario = %s WHERE id = %s""", 
            (request.form['dni'], request.form['nombre'], request.form['apellido'], request.form['telefono'], 
             request.form['email'], request.form['password'], request.form['tipo_usuario'], id))
            mysql.connection.commit()
            flash('Registro actualizado.')
            return redirect(url_for('listar'))
    else:
        flash('Acceso denegado.')
    return render_template('home.html')

@app.route('/eliminar/<string:id>')
def eliminar(id):
    if 'email' in session and session.get('tipo_usuario') == 1:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM clientes WHERE id = %s", (id,))
        mysql.connection.commit()
        flash('Contacto removido.')
        return redirect(url_for('listar'))
    flash('Acceso denegado.')
    return render_template('home.html')

@app.route('/agregarProd', methods=['POST', 'GET'])
def agregarProd():
    if 'email' in session and session.get('tipo_usuario') == 1:
        if request.method == 'POST':
            cur = mysql.connection.cursor()  
            cur.execute("INSERT INTO productos (nombre, precio, descripcion, img, categoria) VALUES (%s, %s, %s, %s, %s)",
            (request.form['nombre'], request.form['precio'], request.form['descripcion'], request.form['img'], request.form['categoria']))
            mysql.connection.commit()
            flash('Producto agregado correctamente!')
        return render_template('agregar.html')
    flash('Acceso denegado.')
    return render_template("home.html")

@app.route('/productos/<string:id>') 
def eliminarProd(id):
    if 'email' in session and session.get('tipo_usuario') == 1:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM productos WHERE id = %s", (id,))
        mysql.connection.commit() 
        flash('Producto eliminado correctamente.')
        return redirect(url_for('productos'))
    flash('Acceso denegado.')
    return render_template("home.html")

# --- RUTAS PRODUCTOS/CONSEJOS (REGISTRADOS) ---
@app.route('/gatos')
def listarG():    
    if 'email' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productos WHERE categoria = 'Gatos'")
        return render_template('gatos.html', productos=cur.fetchall())
    flash('Debe loguearse para ver productos.')
    return redirect(url_for('login'))

@app.route('/perros')
def listarP():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos where categoria = 'Perros'")
    return render_template('perros.html', productos=cur.fetchall())

@app.route('/consejos')
def consejo():
    if 'email' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM consejos")
        return render_template('consejos.html', consejo=cur.fetchall())
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)