import random
import string as st
from urllib.parse import urljoin

from flask import Markup, flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    last_url = [random.choice(st.ascii_letters + st.digits)
                for i in range(6)]
    custom_short = ''.join(last_url)
    if URLMap.query.filter_by(short=custom_short).first():
        return get_unique_short_id()
    return custom_short


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if form.validate_on_submit():

        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if URLMap.query.filter_by(short=custom_id).first() is not None:
            flash(f'Имя {custom_id} уже занято!')

        if not custom_id:
            custom_id = get_unique_short_id()

        if URLMap.query.filter_by(original=original_link).first() is None:

            urlmap = URLMap(
                original=original_link,
                short=custom_id
            )
            db.session.add(urlmap)
            db.session.commit()

        last_url = URLMap.query.filter_by(original=original_link).first()
        original_url = urljoin(request.url, last_url.short)
        message = Markup(f'Ваша ссылка: <a href="{original_url}"'
                         f'target="_blank">{original_url}</a>')
        flash(message, 'info')
    return render_template('index.html', form=form)


@app.route('/<string:id>')
def redirect_url(id):
    url = URLMap.query.filter_by(short=id).first_or_404()
    return redirect(url.original)
