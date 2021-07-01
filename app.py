from flask import Flask
from handlers.main import configure_routes

app = Flask(__name__)
configure_routes(app)

if __name__ == '__main__':
    print("Iniciando ... ")
    app.run(host="0.0.0.0",debug=True)