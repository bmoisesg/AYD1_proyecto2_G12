from flask import Flask
import json

from handlers.main import configure_routes

def test_getProductById_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/producto'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        "id_producto": 112
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_addProductShoppingCart_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/carrito/nuevo'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'id_usuario': 3,
        'id_producto': 112
    }
    response = client.post(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_updateProductQuantity_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/carrito'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'id_usuario': 3,
        'id_producto': 112,
        'cantidad': 8
    }
    response = client.patch(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_delProductFromShoppingCar_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/carrito/producto'

    request_headers = {
        'Content-Type': 'application/json'
    }

    request_data = {
        'id_usuario': 3,
        'id_producto': 112
    }
    response = client.delete(url, data=json.dumps(request_data), headers=request_headers)
    assert response.status_code == 200

def test_getPaymentMethod_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/metodoPago'

    response = client.get(url)
    assert response.status_code == 200

def test_userLogin_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
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
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
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
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
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
    

