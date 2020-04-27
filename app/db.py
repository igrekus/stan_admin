import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


@click.command('reg-user')
@click.option('--user', '-u', 'user')
@click.option('--pw', '-p', 'pw')
@with_appcontext
def reg_user_command(user, pw):
    if not user or not pw:
        click.echo('Need user and password.')
        return

    db = get_db()
    if db.execute('SELECT id FROM user WHERE username = ?', (user,)).fetchone() is not None:
        click.echo(f'User {user} is already registered.')
        return
    db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (user, generate_password_hash(pw)))
    db.commit()
    click.echo(f'New user {user} created.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(reg_user_command)
