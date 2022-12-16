from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import (URL, DataRequired, Length,
                                Optional, Regexp)

from settings import RE_PATTERN


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[URL(), DataRequired('Обязательное поле'), Length(6)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(1, 6),
                    Regexp(RE_PATTERN,
                           message='Введены недопустимые символы')]
    )
    submit = SubmitField('Создать')