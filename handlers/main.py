from typing import cast
from flask import Flask, json, request
from flask.wrappers import Response
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_mail import Mail, Message

import decimal
import base64

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def configure_routes(app):
    CORS(app)
    mysql = MySQL(app)

    app.config['MYSQL_HOST'] = 'mysql-db.crolp0fl8ogz.us-east-2.rds.amazonaws.com'
    app.config['MYSQL_USER'] = 'admin'
    app.config['MYSQL_PASSWORD'] = 'adminy2k'
    app.config['MYSQL_DB'] = 'mydb'

    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'novatech.webstore@gmail.com'
    app.config['MAIL_PASSWORD'] = 'AYD1test'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail = Mail(app)

    @app.route('/', methods=['GET'])
    def index():
        return '<title>Proyecto2</title><h2 style =" text-align: center; line-height: 200px; " > PROYECTO2 AYD1 Y2K </h2> <br><h4>vamos  dormir</h4>'

    # -------------------------------------------------------------------------
    # FUNCION: agregar un nuevo usuario a la base de datos
    # ATRIBUTOS_JSON_ENTADA : nombre, apellido,dpi,email, contrasena, direccion
    # -------------------------------------------------------------------------  
    @app.route('/usuario', methods=['POST'])
    def insert():
        try:    
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
            return Response('usuario ingresado exitosamentes', status=200,mimetype= 'application/text')
        except Exception as e:
            print(e)
            return Response('error al ingresar usuario', status=400, mimetype='application/text')


    # -------------------------------------------------------------------------
    # FUNCION: eliminar todos los productos que tiene el carrito de un usuario
    # ATRIBUTOS_JSON_ENTADA : idusuario
    # -------------------------------------------------------------------------  
    @app.route('/carrito', methods=['DELETE'])
    def eliminarCarrito():
        try:
            contenido = request.json
            idusuario = contenido['idusuario']
            cursor = mysql.connection.cursor()
            cursor.execute(''' delete from carrito where usuario_idusuario = %s ''' , [idusuario])
            cursor.connection.commit()
            cursor.close()
            return Response('carrito limpio' , status=200,mimetype= 'application/text')
        except Exception as e:
            print(e)
            return Response('error al eliminar los productos del carrito', status=400, mimetype='application/text')


    # -------------------------------------------------------------------------
    # FUNCION: retornar todos los productos que tiene el carrito de un usuario
    # ATRIBUTOS_JSON_ENTADA : idusuario
    # -------------------------------------------------------------------------  
    @app.route('/carrito', methods=['POST'])
    def getcarrito():
        contenido = request.json
        idusuario = contenido['idusuario']
        cursor = mysql.connection.cursor()
        cursor.execute(''' select producto_idproducto as idproducto , cantidad from carrito where usuario_idusuario = %s ''' , [idusuario])
        rows = cursor.fetchall()
        cursor.connection.commit()
        cursor.close()
        resjson = json.dumps(rows, cls = Encoder)
        return Response(resjson, status=200,mimetype= 'application/json')

    # -------------------------------------------------------------------------
    # FUNCION: retornar todos los usuarios registrados en el sistema
    # ------------------------------------------------------------------------- 
    @app.route('/usuario')
    def users():
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM usuario''')
        rows = cur.fetchall()
        resjson = json.dumps(rows, cls = Encoder)
        return Response(resjson , status=200,mimetype= 'application/json')

    # -------------------------------------------------------------------------
    # FUNCION: retornar todos los productos registrados en el sistema
    # ------------------------------------------------------------------------- 
    @app.route('/producto')
    def gettodosProductos():
        cur = mysql.connection.cursor()
        cur.execute('''select *  from producto''')
        rows = cur.fetchall()
        resjson = json.dumps(rows, cls = Encoder)
        return Response(resjson, status=200,mimetype= 'application/json')

    # -------------------------------------------------------------------------
    # FUNCION: eliminar un usuario segun su email
    # ------------------------------------------------------------------------- 
    @app.route('/usuario', methods=['DELETE'])
    def eliminarUsuario():
        cur = mysql.connection.cursor()
        contenido = request.json
        email = contenido['email']
        cur.execute('''delete from usuario where email = %s''',[email])
        cur.connection.commit()
        return Response("usuario eliminado", status=200,mimetype= 'application/text')

    # -------------------------------------------------------------------------
    # FUNCION: llenar el detalle de la factura, primero ingresar los productos 
    #          que tiene el carrito en la tabla detallefactura, elimina los 
    #          productos del carrito y actualiza el stock del producto
    # ATRIBUTOS_JSON_ENTADA : idusuario , idfactura
    # ------------------------------------------------------------------------- 
    @app.route('/detalleFactura',methods=['POST'])
    def setdetalleFactura():
        contenido = request.json
        idusuario = contenido['idusuario']
        idfactura = contenido['idfactura']
        # 1. traer los productos del carrito del usuario
        cur = mysql.connection.cursor()
        cur.execute(''' select producto_idproducto, cantidad from carrito where usuario_idusuario = %s ''' , [idusuario])
        rows = cur.fetchall()
        # 2. iterar cada uno de los elementos y pasarlos a detallefactura, tambien actualizar el stock por cada iteracion
        for element in rows:
            print(element[0]) # producto
            print(element[1]) # cantidad
            cur.execute(''' insert into detalleFactura (factura_idfactura, producto_idproducto, cantidad) values (%s,%s,%s) ''' , [str(idfactura),str(element[0]),str(element[1])])
            cur.execute(''' update producto set stock = stock - %s where idproducto = %s ''', [str(element[1]),str(element[0])])
            cur.connection.commit()
        # 3. eliminar todos los productos que tenia en el carrito
        cur.execute(''' delete from carrito where usuario_idusuario = %s ''' , [idusuario])
        cur.connection.commit()
        cur.close()
        return Response('Realizado con exito', status=200,mimetype= 'application/text')
    
    # -------------------------------------------------------------------------
    # FUNCION: retornar toda la informacion de una factura con solo enviar el id
    # ------------------------------------------------------------------------- 
    @app.route('/infofactura',methods=['POST'])
    def getInfoFactura():
        contenido = request.json
        idfactura = contenido['idfactura']
        cur = mysql.connection.cursor()
        cur.execute('''select producto_idproducto as idproducto, cantidad from detalleFactura where factura_idfactura = %s ''',[idfactura])
        rows = cur.fetchall()
        retornarjson=[]
        retornarjson.append(rows)
        cur.execute('''select * from factura where idfactura = %s ''',[idfactura])
        rows = cur.fetchall()
        retornarjson.append(rows)
        resjson = json.dumps(retornarjson, cls = Encoder)

        return Response(resjson, status=200,mimetype= 'application/json')


    #---------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------------------


    # Insertar un producto
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
    @app.route('/carrito/producto', methods=['POST'])
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

            query = '''SELECT idusuario, nombre FROM usuario WHERE email = %s AND contrasena = %s'''
            values = (email,password)

            cursor.execute(query, values)
            result = cursor.fetchall()

            resjson = json.dumps(result[0], cls = Encoder)
            print(resjson)
            return Response(resjson, status=200, mimetype='application/json')
        except Exception as e:
            print('[ERROR]:',e)
            return Response('{"msg":"Usuario no autorizado."}', status=401, mimetype='application/json')
        finally:
            cursor.close()

    # Ingresar los datos de facturación en la entidad
    @app.route('/factura', methods=['POST'])
    def setBillInformation():
        try:
            cursor = mysql.connection.cursor()
            nit = request.json['nit']
            fecha = request.json['fecha']
            telefono = request.json['telefono']
            usuario = request.json['id_usuario']
            total = request.json['total']

            # Query que inserta los datos de facturación 
            query = '''INSERT INTO factura (nit, fecha, telefono, usuario_idusuario, total)
                    VALUES (%s,%s,%s,%s,%s)'''
            values = (nit,fecha,telefono,int(usuario),float(total));

            cursor.execute(query, values)
            cursor.connection.commit()

            # Query que obtiene la última factura insertada.
            query = '''SELECT LAST_INSERT_ID()'''
            cursor.execute(query)
            result = cursor.fetchall()

            resjson = json.dumps(result[0], cls = Encoder)
            print('ID factura:',resjson)
            return Response(resjson, status=200, mimetype='application/json')
        except Exception as e:
            print('[ERROR]:',e)
            return Response('{"msg":"Error al insertar datos de facturación."}', status=400, mimetype='application/json')
        finally:
            cursor.close()

    # Ingresar los datos de facturación en la entidad
    @app.route('/factura/detallePago', methods=['POST'])
    def setPaymentDetail():
        try:
            cursor = mysql.connection.cursor()
            metodo = request.json['metodo_pago']
            factura = request.json['id_factura']
            numero = request.json['numero_tarjeta']
    
            query = '''INSERT INTO detallemetodoPago (metodoPago_idtarjeta, factura_idfactura, numero)
                    VALUES (%s,%s,%s)'''
            values = (int(metodo), int(factura), numero);

            cursor.execute(query, values)
            cursor.connection.commit()

            return Response('{"msg":"Información de pago almacenada."}', status=200, mimetype='application/json')
        except Exception as e:
            print('[ERROR]:',e)
            return Response('{"msg":"Error al insertar información de pago."}', status=400, mimetype='application/json')
        finally:
            cursor.close()
    
    #Ruta test de correos electronicos
    @app.route('/email', methods=['GET'])
    def testEmail():
        msg = Message('Hello', sender = 'novatech.webstore@gmail.com', recipients = ['byron.alvamora@gmail.com'])
        msg.body = "Hola desde Flask..."
        mail.send(msg)
        return "Sent", 200
    
    #Ruta test de correos electronicos
    @app.route('/email', methods=['POST'])
    def sendEmail():
        email = request.json['email']
        billb64 = request.json['factura_b64']

        with open('bills/temp.pdf', 'wb') as f:
            f.write(base64.b64decode(billb64))

        """ msg = Message('Factura', sender = 'novatech.webstore@gmail.com', recipients = [email])
        msg.body = "Hola desde Flask..."
        mail.send(msg) """
        return "Sent", 200

     
