from flask import Flask
from flask.globals import request
import json

from handlers.main import configure_routes

app = Flask(__name__)
configure_routes(app)
client = app.test_client()

def test_getProductById_route():
    url = '/producto'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        "id_producto": 49
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_addProductShoppingCart_route():
    url = '/carrito/nuevo'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'id_usuario': 3,
        'id_producto': 49
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_updateProductQuantity_route():
    url = '/carrito'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'id_usuario': 3,
        'id_producto': 49,
        'cantidad': 8
    }
    response = client.patch(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_delProductFromShoppingCar_route():
    url = '/carrito/producto'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'id_usuario': 3,
        'id_producto': 49
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_getPaymentMethod_route():
    url = '/metodoPago'

    response = client.get(url)
    assert response.status_code == 200

def test_userLogin_route():
    url = '/usuario/sesion'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'email': 'mymail@gmail.com',
        'password': 'mypassword'
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_setBillInformation_route():
    url = '/factura'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'nit': '745688912',
        'fecha': '2021-06-20 11:28:35',
        'telefono': '55002020',
        'id_usuario': 3,
        'total': 44.25
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_setPaymentDetail_route():
    url = '/factura/detallePago'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'metodo_pago': 3,
	    'id_factura': 1,
	    'numero_tarjeta': '500 7910 990 12'
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200
    

def test_ingresarUsuario():
    info= {
	        "nombre":"nombrePrueba",
	        "apellido":"apellidoPrueba",
	        "dpi":"dpiPrueba",
	        "email":"correoPrueba",
	        "contrasena":"contraPrueba",
	        "direccion":"direccionPrueba"
    }
    response = client.post("/usuario", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
    if response.status_code == 200:
        objeto={
            "email": "correoPrueba"
        }
        response = client.delete("/usuario", data=json.dumps(objeto), headers={'Content-Type': 'application/json'})

def test_eliminarcarrito():
    info= {
	        "idusuario":"0"
    }
    response = client.delete("/carrito", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    assert response.data == b"carrito limpio"

def test_traerElementosCarrito():
    info= { "idusuario":"0" }
    response = client.post("/carrito", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

def test_getusuarios():
    response = client.get("/usuario")
    assert response.status_code == 500

def test_getproductos():
    response = client.get("/producto")
    assert response.status_code == 200

def test_eliminarUsuario():
    info={ "email":"test" } 
    response = client.delete("/usuario", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

def test_retornardetallefactura():
    info={ "idfactura":"0" } 
    response = client.post("/infofactura", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

def test_ingresardetallefactura():
    info={ "idfactura":"0" , "idusuario":"0"} 
    response = client.post("/detalleFactura", data=json.dumps(info), headers={'Content-Type': 'application/json'})
    assert response.status_code == 200
