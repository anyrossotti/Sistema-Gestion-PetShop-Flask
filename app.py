import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde el archivo .env local

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave_por_defecto_si_no_hay_env')
mysql = MySQL(app)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 3306))

# Agrego la ruta, la barra corresponde a local host
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

def refugio():
    return render_template('https://www.facebook.com/hogarsilgassman/')

# Listado de Usuarios
@app.route('/listado', methods=['POST', 'GET'])
def listar():
    if request.method == 'GET':
        if 'email' in session and session['tipo_usuario'] == 1:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM clientes")
            datos = cur.fetchall() 
            print(datos)
            return render_template('listado.html', clientes=datos)
        else:
            message = 'Error de Acceso. Debe tener permisos de administrador para poder acceder.'
            flash(message)
            return render_template("home.html")

# Registro, Login, Salir de Sesión Usuario
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        consulta = cur.execute("SELECT * FROM clientes WHERE email = %s AND password = %s", [email, password])
        user = cur.fetchone()
        mysql.connection.commit()
        if user != 0 and user is not None:
            session['logged_in'] = True
            session['email'] = user[5]
            session['tipo_usuario'] = user[6] # tipo_usuario
            if session['tipo_usuario'] == 0:
                message = "Acceso Correcto! Ahora podés disfrutar de nuestros productos"
                flash(message)
                return render_template('home.html')
            elif session['tipo_usuario'] == 1:
                message = "Acceso Correcto a las funciones de Administrador."
                flash(message)
                return render_template('admin.html')
        else:
            message = "Error de acceso. No existe el usuario"
            flash(message)
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/registro', methods=["GET", "POST"])
def registro():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes")
    cliente = cur.fetchall()
    if request.method == 'GET':
        return render_template("registro.html", clientes=cliente)
    else:
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        tipo_usuario = 0
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clientes(dni, nombre, apellido, telefono, email, password, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (dni, nombre, apellido, telefono, email, password, tipo_usuario))
        mysql.connection.commit()
        return redirect(url_for('login'))

@app.route('/salir', methods=["GET", "POST"])
def salir():
    session.clear()
    session['logged_in'] = False
    return render_template("home.html")
    
# Traer la info, para despues editar
@app.route('/obtenerCliente/<id>')
def obtenerCliente(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes where id = %s" % (id))
    datos = cur.fetchall()
    return render_template('editar.html', clientes=datos[0])
    
# Actualizar, editar info de usuario por id
@app.route('/actualizar/<id>', methods=['POST','GET'])
def actualizar(id):
    if request.method == 'POST':
        if 'email' in session and session['tipo_usuario'] == 1:
            dni = request.form['dni']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            telefono = request.form['telefono']
            email = request.form['email']
            password = request.form['password']
            tipo_usuario = request.form['tipo_usuario']
            cur = mysql.connection.cursor()  
            cur.execute("""UPDATE clientes SET dni = %s, 
            nombre = %s, apellido = %s, telefono = %s, 
            email = %s, password = %s, tipo_usuario = %s WHERE id = %s""", (dni, nombre, apellido, telefono, email, password, tipo_usuario, id))
            mysql.connection.commit()
            message = 'Registro actualizado.'
            flash(message)
            return redirect(url_for('listar'))
        else:
            message = 'Debe tener permisos de Administrador para poder acceder.'
            flash(message)
            return render_template('home.html')

# Eliminar usuario por id
@app.route('/eliminar/<string:id>')
def eliminar(id):
    if 'email' in session and session['tipo_usuario'] == 1:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM clientes where id = %s" % (id))
        mysql.connection.commit()
        message = 'Contacto removido correctamente.'
        flash(message)
        return redirect(url_for('listar'))
    else:
        message = 'Debe tener permisos de Administrador para poder acceder.'
        flash(message)
        return render_template('home.html')

# Buscar usuario por id
@app.route('/busquedaID/<id>', methods=['POST', 'GET'])
def buscarID(id):
    if request.method == 'POST':
        id = request.form['id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = %s" % (id))
        datos = cur.fetchall() 
        return render_template('busquedaID.html', clientes=datos[0])

# Buscar usuario por DNI
@app.route('/busquedaDNI/<dni>', methods=['POST', 'GET'])
def buscarDNI(dni):
    if request.method == 'POST':
        dni = request.form['dni']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes WHERE dni = %s" % (dni))
        datos = cur.fetchall() 
        return render_template('busquedaDNI.html', clientes=datos[0])
    
# Funciones de Productos
@app.route('/gatos', methods=['POST', 'GET'])
def listarG():    
    if request.method == 'GET':
        if 'email' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM productos WHERE categoria = 'Gatos'")
            datos = cur.fetchall() 
            print(datos)
            return render_template('gatos.html', productos=datos)
        else:
            message = 'Error de Acceso. Debe Loguearse/Registrarse para poder ver los productos.'
            flash(message)
            return render_template("login.html")

@app.route('/perros')
def listarP():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM productos where categoria = 'Perros'")
        datos = cur.fetchall() 
        print(datos)
        return render_template('perros.html', productos=datos)

@app.route('/otros')
def listarO():
    if request.method == 'GET':
        if 'email' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM productos WHERE categoria = 'Otros'")
            datos = cur.fetchall() 
            print(datos)
            return render_template('otros.html', productos=datos)
        else:
            message = 'Error de Acceso. Debe Loguearse/Registrarse para poder ver los productos.'
            flash(message)
            return render_template("login.html")
    
@app.route('/agregarProd', methods=['POST', 'GET'])
def agregarProd():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        img = request.form['img']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()  
        cur.execute("INSERT INTO productos (nombre, precio, descripcion, img, categoria) VALUES (%s, %s, %s, %s, %s)",
        (nombre, precio, descripcion, img, categoria))
        mysql.connection.commit()
        message = 'Producto agregado correctamente!'
        flash(message)
    return render_template('agregar.html')

@app.route('/productos/<string:id>') 
def eliminarProd(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s" % (id))
    mysql.connection.commit() 
    message = 'Producto eliminado correctamente.'
    flash(message)
    return redirect(url_for('productos'))

@app.route('/obtenerProducto/<id>', methods=['POST','GET'])
def obtProd(id):
    if request.method == 'GET':
        if 'email' in session and session['tipo_usuario'] == 1:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM productos where id = %s" % (id))
            datos = cur.fetchall()
            return render_template('editarProd.html', producto=datos[0])
        else:
            message = 'Error de Acceso. Debe Tener permisos de administrador para poder ingresar.'
            flash(message)
            return render_template("home.html")

@app.route('/editarProducto/<id>', methods=['POST','GET'])
def editarProd(id):
    if request.method == 'POST':
        if 'email' in session and session['tipo_usuario'] == 1:
            nombre = request.form['nombre']
            precio = request.form['precio']
            descripcion = request.form['descripcion']
            cur = mysql.connection.cursor()  
            cur.execute("""UPDATE productos SET nombre = %s, 
            precio = %s, descripcion = %s WHERE id = %s""", 
            (nombre, precio, descripcion, id))
            mysql.connection.commit()
            message = 'Producto actualizado.'
            flash(message)
            return redirect(url_for('productos'))
        else:
            message = 'Error de Acceso. Debe Tener permisos de administrador para poder ingresar.'
            flash(message)
            return render_template("home.html")

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'GET':
        if 'email' in session and session['tipo_usuario'] == 1:
            return render_template('admin.html')
        else:
            message = 'Error de Acceso. Debe Tener permisos de administrador para poder ingresar.'
            flash(message)
            return render_template("home.html")

@app.route('/agregarAdmin', methods=['POST', 'GET'])
def agregar():
    if 'email' in session and session['tipo_usuario'] == 1:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        cliente = cur.fetchall()
        if request.method == 'GET':
            return render_template("agregarAdmin.html", clientes=cliente)
        else:
            dni = request.form['dni']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            telefono = request.form['telefono']
            email = request.form['email']
            password = request.form['password']
            tipo_usuario = request.form['tipo_usuario']
            cur = mysql.connection.cursor()  
            cur.execute("INSERT INTO clientes(dni, nombre, apellido, telefono, email, password, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (dni, nombre, apellido, telefono, email, password, tipo_usuario))
            mysql.connection.commit()
            message = 'Usuario/Administrador agregado correctamente.'
            flash(message)
            return render_template('admin.html')
    else:
        message = 'Error de Acceso. Debe Tener permisos de administrador para poder ingresar.'
        flash(message)
        return render_template("home.html")

@app.route('/productos', methods=['POST', 'GET'])
def productos():
    if request.method == 'GET':
        if 'email' in session and session['tipo_usuario'] == 1:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM productos")
            datos = cur.fetchall() 
            print(datos)
            return render_template('productos.html', productos=datos)
        else:
            message = 'Error de Acceso. Debe Tener permisos de administrador para poder ingresar.'
            flash(message)
            return render_template("home.html")

@app.route('/consejos', methods=['POST', 'GET'])
def consejo():
    if request.method == 'GET':
        if 'email' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM consejos")
            datos = cur.fetchall()
            return render_template('consejos.html', consejo=datos)
        else:
            message = 'Error de Acceso. Debe Loguearse/Registrarse para poder acceder a esta sección.'
            flash(message)
            return redirect(url_for('login'))

@app.route('/consejos/<id>', methods=['POST', 'GET'])
def contenido(id):
    if request.method == 'GET':
        if 'email' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM consejos WHERE id = %s" % (id))
            datos = cur.fetchall()
            return render_template('consejos_contenido.html', consejo=datos)

if __name__ == '__main__':
    app.run(debug=True)