from flask import Flask
import json

from handlers.main import configure_routes

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

