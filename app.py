from flask import Flask
from config import configure_app
from routes import init_routes

app = Flask(__name__)
configure_app(app)
init_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
