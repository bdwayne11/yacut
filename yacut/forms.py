from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[URL(), DataRequired('Обязательное поле'), Length(6)]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(1, 6)]
    )
    submit = SubmitField('Создать')