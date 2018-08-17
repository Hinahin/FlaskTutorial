from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Regexp
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')


class GradeReportForm(FlaskForm):
    course_name = StringField('Название курса', validators=[DataRequired()])
    session_course = StringField('Запуск курса', validators=[DataRequired()])
    date_report = DateField('Дата выгрузки', format='%d.%m.%Y', validators=[DataRequired()])
    file_report = FileField('Файл для загрузки(.csv)', validators=[FileRequired(),
                                                                   FileAllowed(['csv'],
                                                                               'CSV Only')
                                                                   ])
    submit = SubmitField('Добавить')
