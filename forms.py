from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, NumberRange, Email


class UserForm2(FlaskForm):

    matricula = StringField("matricula")
   
    nombre = StringField('nombre')

    apellidos = StringField('apellidos', [
        DataRequired(message='El apellido es requerido')
    ])

    email = EmailField('correo')
    telefono = StringField("Teléfono")

    especialidad = StringField('especialidad')

class InscripcionForm(FlaskForm):
    pass