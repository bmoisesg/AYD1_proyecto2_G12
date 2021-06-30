from flask import Flask
import json

from flask.globals import request

from handlers.main import configure_routes

app = Flask(__name__)
configure_routes(app)
client = app.test_client()

def test_addProduct_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/producto/nuevo'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'nombre': 'Unit-Test',
        'descripcion': 'Unit Test Pytest',
        'precio': 25.5,
        'peso': 0.8,
        'stock': 15,
        'id_categoria': 2,
        'nombre_img': 'test-0.jpg'
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
    assert response.status_code == 200

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