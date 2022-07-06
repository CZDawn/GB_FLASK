import os
from PIL import Image
from flask import current_app, url_for
from secrets import token_hex
from flask_mail import Message

from test_flask_lesson import mail


def save_picture(form_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path,
        'static/profile_pics',
        picture_fn
    )
    output_size = (150, 150)
    image_obj = Image.open(form_picture)
    image_obj.thumbnail(output_size)
    image_obj.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message(
        'Request for reset password',
        sender='badrhymes@yandex.ru',
        recipients=[user.email]
    )
    message.body = f'''To reset password, click on the link: 
        {url_for('users.reset_token', token=token, _external=True)}.
        If you didnt do this request then just ignore this message.'''
    mail.send(message)

