from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError

from test_flask_lesson.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username:',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email:',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password:',
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm password:',
        validators=[DataRequired(), EqualTo('password')]
    )
    role = StringField(
        'Role:',
        validators=[DataRequired(), Length(min=2, max=80)]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя занято. Выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email занят. Выбкрите другой.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email:',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password:',
        validators=[DataRequired()]
    )
    remember = BooleanField('Remember password')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    picture = FileField(
        'Update profile photo',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. Выберите другое.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email занят. Выберите другой.')


class RequestResetPasswordForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    submit = SubmitField('Change password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'Аккаунт с данным email-адресом отсутствует. '
                'Вы можете зарегистрировать его.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset password')
