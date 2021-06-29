from flask import Flask, json, request, jsonify
from flask.wrappers import Response
from flask_mysqldb import MySQL
from flask_cors import CORS

import decimal

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'mysql-db.crolp0fl8ogz.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminy2k'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

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


@app.route('/productos',methods=['POST'])
def getproductos():
    cur = mysql.connection.cursor()
    cur.execute('''select (count(*) div 10)+1  from producto''')
    rows = cur.fetchall()
    return jsonify(rows[0])

# Insertar un producto en la entidad 
@app.route('/producto/nuevo', methods=['POST'])
def addProduct():
    try:
        cursor = mysql.connection.cursor()
        name = request.json['nombre']
        description = request.json['descripcion']
        price = request.json['precio']
        weight = request.json['peso']
        stock = request.json['stock']
        category = request.json['id_categoria']
        image = request.json['nombre_img']

        query = '''INSERT INTO producto (nombre, descripcion, precio, peso, stock, categoria_idcategoria, nombreImagen)
                VALUES(%s,%s,%s,%s,%s,%s,%s)'''
        values = (name,description,float(price),float(weight),int(stock),int(category),image)

        cursor.execute(query, values)
        cursor.connection.commit()
        return Response('{"msg":"Producto insertado exitosamente."}', status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"Error al insertar producto."}', status=400, mimetype='application/json')
    finally:
        cursor.close()

# Insertar un producto al carrito de compras
@app.route('/carrito/nuevo', methods=['POST'])
def addProductShoppingCar():
    try:
        cursor = mysql.connection.cursor()
        iduser = request.json['id_usuario']
        idproduct = request.json['id_producto']

        query = '''INSERT INTO carrito (producto_idproducto, usuario_idusuario, cantidad)
                VALUES(%s,%s,%s)'''
        values = (int(idproduct), int(iduser), 1)

        cursor.execute(query, values)
        cursor.connection.commit()
        return Response('{"msg":"Producto añadido a carrito."}', status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"Error al añadir producto al carrito."}', status=400, mimetype='application/json')
    finally:
        cursor.close()

# Obtener producto por ID
@app.route('/producto', methods=['POST'])
def getProductById():
    try:
        cursor = mysql.connection.cursor()
        idproduct = request.json['id_producto']

        query = '''SELECT * FROM producto WHERE idproducto = %s'''

        cursor.execute(query, [idproduct])
        result = cursor.fetchall()

        resjson = json.dumps(result[0], cls = Encoder)
        return Response(resjson, status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"Producto no encontrado."}', status=404, mimetype='application/json')
    finally:
        cursor.close()

# Obtener todos los tipos de métodos de pago
@app.route('/metodoPago', methods=['GET'])
def getPaymentMethod():
    try:
        cursor = mysql.connection.cursor()

        query = '''SELECT * FROM metodoPago;'''

        cursor.execute(query)
        result = cursor.fetchall()

        resjson = json.dumps(result, cls = Encoder)
        return Response(resjson, status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"Error al obtener metodos de pago."}', status=400, mimetype='application/json')
    finally:
        cursor.close()

# Eliminar producto del carrito del usuario
@app.route('/carrito/producto', methods=['DELETE'])
def delProductFromShoppingCar():
    try:
        cursor = mysql.connection.cursor()
        iduser = request.json['id_usuario']
        idproduct = request.json['id_producto']

        query = '''DELETE FROM carrito
                   WHERE producto_idproducto = %s AND usuario_idusuario = %s'''
        values = (int(idproduct), int(iduser))

        cursor.execute(query, values)
        cursor.connection.commit()
        return Response('{"msg":"Producto eliminado del carrito."}', status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"No se pudo eliminar el producto del carrito."}', status=400, mimetype='application/json')
    finally:
        cursor.close()

# Eliminar producto del carrito del usuario
@app.route('/carrito', methods=['PATCH'])
def updateProductQuantity():
    try:
        cursor = mysql.connection.cursor()
        iduser = request.json['id_usuario']
        idproduct = request.json['id_producto']
        quantity = request.json['cantidad']

        query = '''UPDATE carrito
                   SET cantidad = %s
                   WHERE producto_idproducto = %s AND usuario_idusuario = %s;'''
        values = (int(quantity), int(idproduct), int(iduser))

        cursor.execute(query, values)
        cursor.connection.commit()
        return Response('{"msg":"Producto actualizado en el carrito."}', status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"No se pudo actualizar el producto del carrito."}', status=400, mimetype='application/json')
    finally:
        cursor.close()

# Valida el inicio de sesión de un usuario
@app.route('/usuario/sesion', methods=['POST'])
def userLogin():
    try:
        cursor = mysql.connection.cursor()
        email = request.json['email']
        password = request.json['password']

        query = '''SELECT * FROM usuario WHERE email = %s AND contrasena = %s'''
        values = (email,password)

        cursor.execute(query, values)
        result = cursor.fetchall()

        resjson = json.dumps(result[0], cls = Encoder)
        print(resjson)
        return Response('{"msg":"Usuario válido."}', status=200, mimetype='application/json')
    except Exception as e:
        print('[ERROR]:',e)
        return Response('{"msg":"Usuario no autorizado."}', status=401, mimetype='application/json')
    finally:
        cursor.close()

if __name__ == '__main__':
    print("iniciando ... ")
    app.run(host="0.0.0.0",debug=True)