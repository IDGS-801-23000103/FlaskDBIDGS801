from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email


class UserForm2(FlaskForm):

    id = IntegerField('id', [
        NumberRange(min=1, max=20, message='Valor no válido')
    ])

    nombre = StringField('nombre', [
        DataRequired(message='El nombre es requerido'),
        Length(min=4, max=20, message='Requiere mínimo 4 y máximo 20')
    ])

    apaterno = StringField('apaterno', [
        DataRequired(message='El apellido es requerido')
    ])

    email = EmailField('correo', [
        DataRequired(message='El correo es requerido'),
        Email(message='Ingresa un correo válido')
    ])
