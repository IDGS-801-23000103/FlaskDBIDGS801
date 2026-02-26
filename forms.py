from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email


class UserForm2(FlaskForm):

   
    nombre = StringField('nombre', [
        DataRequired(message='El nombre es requerido'),
        Length(min=4, max=20, message='Requiere mínimo 4 y máximo 20')
    ])

    apellidos = StringField('apellidos', [
        DataRequired(message='El apellido es requerido')
    ])

    email = EmailField('correo', [
        DataRequired(message='El correo es requerido'),
        Email(message='Ingresa un correo válido')
    ])
