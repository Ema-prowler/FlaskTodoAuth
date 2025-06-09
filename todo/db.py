import mysql.connector

import click # esto nos va ayudar a para poder ejecutar comandos en la terminal

from flask import current_app, g  # Current app mantiene la aplicacion que estamos ejecutando
from flask.cli import with_appcontext # esto nos va a servir cuando nosotros estemos ejecuntando el script de base de datos (para contexto)
from .schema import instructions # Schema contenera todos los script para poder crear la base de datos

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

# Cerrar la conexion de la base de datos cada vez que nostros hagamos una peticion:

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

@click.command('init_db')
@with_appcontext

def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)