from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('quote', __name__, url_prefix='/quote')


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    quotes = db.execute(
        'SELECT q.id, q.message_id, q.text'
        ' FROM quote q'
        ' ORDER BY q.id DESC'
    ).fetchall()
    return render_template('quote/index.html', quotes=reversed(quotes))


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        message_id = request.form['message_id']
        text = request.form['text']
        error = None

        if not text:
            error = 'Quote text is required.'
        if message_id:
            try:
                message_id = int(message_id)
            except ValueError:
                error = 'message_id should be an int.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO quote (message_id, text)'
                ' VALUES (?, ?)',
                (message_id if message_id else None, text)
            )
            db.commit()
            return redirect(url_for('quote.index'))

    return render_template('quote/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    quote = dict(get_quote(id))

    if quote['message_id'] is None:
        quote['message_id'] = ''

    if request.method == 'POST':
        message_id = request.form['message_id']
        text = request.form['text']
        error = None

        if not text:
            error = 'Quote text is required.'
        if message_id:
            try:
                message_id = int(message_id)
            except ValueError:
                error = 'message_id should be an int.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE quote SET message_id = ?, text = ?'
                ' WHERE id = ?',
                (message_id if message_id else None, text, id)
            )
            db.commit()
            return redirect(url_for('quote.index'))

    return render_template('quote/update.html', quote=quote)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_quote(id)
    db = get_db()
    db.execute('DELETE FROM quote WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('quote.index'))


def get_quote(id):
    quote = get_db().execute(
        'SELECT q.id, q.message_id, q.text'
        ' FROM quote AS q'
        ' WHERE q.id = ?',
        (id,)
    ).fetchone()
    if quote is None:
        abort(404, f"Quote id {id} doesn't exist.")
    return quote
