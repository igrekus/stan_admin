import os

from flask import Flask, redirect, url_for, g, render_template, flash
from flask_restful import Api

from . import db
from .api_endpoints import ApiPing, Login, LoggedUser


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, '../../stan_bot/quotes.db')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def index():
        if g.user:
            return redirect(url_for('quote.index'))
        else:
            return render_template('base.html')

    @app.route('/api/delete/<int:quote_id>', methods=('GET', 'POST'))
    def api_delete(quote_id):
        conn = db.get_db()
        res = db.get_db().execute('DELETE FROM quote WHERE id = ?', (quote_id,))
        conn.commit()
        if res.rowcount:
            flash(f'Deleted quote {quote_id}')
            return {'ok': 1, 'deleted': f'{quote_id}'}
        return {'ok': 0}

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import quote
    app.register_blueprint(quote.bp)

    api = Api(app)
    api.add_resource(ApiPing, '/api')
    api.add_resource(Login, '/api/login')
    api.add_resource(LoggedUser, '/api/logged')
    return app
