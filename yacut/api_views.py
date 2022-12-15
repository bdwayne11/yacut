import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidApiUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():

    data = request.get_json()

    if data is None:
        raise InvalidApiUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidApiUsage('"url" является обязательным полем!')

    # if URLMap.query.filter_by(original=data['url']).first() is None: # Проверка на уникальность ссылки original
    custom_id = data.get('custom_id')

    if custom_id:
        if len(custom_id) > 16 or not re.match('^[A-Za-z0-9]*$',
                                               custom_id):
            raise InvalidApiUsage('Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(
                short=custom_id).first():  # Проверка короткой ссылки на уникальность
            raise InvalidApiUsage(f'Имя "{custom_id}" уже занято.', 400)

    else:
        custom_id = get_unique_short_id()

    url = URLMap(
        original=data['url'],
        short=custom_id
    )

    db.session.add(url)
    db.session.commit()

    return jsonify(url.to_dict()), 201

    # return jsonify(URLMap.query.filter_by(original=data['url']).first().to_dict())


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()

    if url is None:
        raise InvalidApiUsage('Указанный id не найден', 404)

    return jsonify(dict(url=url.original)), 200