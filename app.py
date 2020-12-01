from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#mysql conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'productosPRYT'
mysql = MySQL(app)
#sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    #print(data)
    return render_template("index.html", productos=data)

@app.route('/add_product', methods=['POST'])
def addproduct():
    if request.method == 'POST':
        nompr = request.form['nompr']
        preciopr = request.form['preciopr']
        categoriapr = request.form['categoriapr']
        fechaexppr = request.form['fechaexppr']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (nombre,precio,categoria,fechaexp) values (%s, %s, %s, %s)',
                    (nompr, preciopr, categoriapr, fechaexppr))
        mysql.connection.commit()
        flash('Producto agregado satisfactoriamente')
    return redirect(url_for('index'))

@app.route('/edit/<id>')
def obtenerProductos(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE idproductos = %s", (id))
    data = cur.fetchone()
    #print(data)
    return render_template('edit-pr.html', productos = data)

@app.route('/update/<id>', methods=['POST'])
def actualizarProd(id):
    if request.method == 'POST':
        nompr = request.form['nompr']
        preciopr = request.form['preciopr']
        categoriapr = request.form['categoriapr']
        fechaexppr = request.form['fechaexppr']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE productos SET nombre = %s,
            precio = %s,
            categoria = %s,
            fechaexp = %s
        WHERE idproductos = %s
        """, (nompr, preciopr, categoriapr, fechaexppr, id))
        mysql.connection.commit()
        flash('producto actualizado satisfactoriamente')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def borrarProductos(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE idproductos = {0}".format(id))
    mysql.connection.commit()
    flash('producto removido satisfactoriamente!')
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
