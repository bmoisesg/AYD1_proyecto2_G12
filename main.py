from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql-db.crolp0fl8ogz.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminy2k'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def index():
    return '<title>Proyecto2</title><h2 style =" text-align: center; line-height: 200px; " > PROYECTO2 AYD1 Y2K </h2>'

@app.route('/usuario', methods=['POST'])
def insert():
    contenido = request.json
    nombre = contenido['nombre']
    apellido = contenido['apellido']
    dpi = contenido['dpi']
    email = contenido['email']
    contrasena = contenido['contrasena']
    direccion = contenido['direccion']
 
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO usuario(nombre,apellido,dpi,email,contrasena,direccion) VALUES(%s,%s,%s,%s,%s,%s) ''' , [nombre,apellido,dpi,email,contrasena,direccion])
    cursor.connection.commit()
    cursor.close()
    return 'usuario ingresado'


@app.route('/carrito', methods=['DELETE'])
def eliminarCarrito():
    contenido = request.json
    idusuario = contenido['idusuario']
    cursor = mysql.connection.cursor()
    cursor.execute(''' delete from carrito where usuario_idusuario = %s ''' , [idusuario])
    cursor.connection.commit()
    cursor.close()
    return 'carrito limpio'


@app.route('/carrito', methods=['POST'])
def getcarrito():
    contenido = request.json
    idusuario = contenido['idusuario']
    cursor = mysql.connection.cursor()
    cursor.execute(''' select producto_idproducto as idproducto from carrito where usuario_idusuario = %s ''' , [idusuario])
    rows = cursor.fetchall()
    cursor.connection.commit()
    cursor.close()
    return jsonify(rows)


@app.route('/usuario')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM usuario''')
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/numpageproducto')
def getnumpage():
    cur = mysql.connection.cursor()
    cur.execute('''select (count(*) div 10)+1  from producto''')
    rows = cur.fetchall()
    return jsonify(rows[0])


@app.route('/producto',methods=['POST'])
def getproductos():
    cur = mysql.connection.cursor()
    cur.execute('''select (count(*) div 10)+1  from producto''')
    rows = cur.fetchall()
    return jsonify(rows[0])


if __name__ == '__main__':
    print("iniciando ... ")
    app.run(host="0.0.0.0",debug=True)