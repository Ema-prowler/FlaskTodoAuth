import os # Importamos "os" que nos sirve para acceder a ciertas cosas del sistema operativo, en este caso (Variables de entorno)

from flask import Flask         #

def create_app():               #   Usamos esta funcion para crear instancias direfentes de la misma
    app = Flask(__name__)       #   Todas las aplicaciones que creamos en Flask son una instancia de Flask

    app.config.from_mapping(
        SECRET_KEY='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
    )

    from . import db

    db.init_app(app)

    from . import auth

    app.register_blueprint(auth.bp)

    @app.route('/hola')
    def hola():
        return 'Ema feliz'
    
    return app