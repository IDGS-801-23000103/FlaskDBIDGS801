from flask_sqlalchemy import SQLAlchemy

import datetime


db = SQLAlchemy()
inscripcion = db.Table('inscripcion',
    db.Column('alumno_id', db.Integer, db.ForeignKey('alumnos.id')),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id')),
    db.UniqueConstraint('alumno_id', 'curso_id')
)

class Alumnos(db.Model):
    __tablename__='alumnos'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    apellidos=db.Column(db.String(200))
    email=db.Column(db.String(120))
    telefono = db.Column(db.String(20))
    created_data=db.Column(db.DateTime, default=datetime.datetime.now)

    cursos = db.relationship(
        'Curso',
        secondary=inscripcion,
        back_populates="alumnos"
    )



class Maestros(db.Model):
    __tablename__ = 'maestros'
    matricula= db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
    cursos = db.relationship('Curso', back_populates="maestro")
    

class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    maestro_id = db.Column(
        db.Integer,
        db.ForeignKey('maestros.matricula')
    )

    maestro = db.relationship(
        'Maestros',
        back_populates="cursos"
    )

    alumnos = db.relationship(
        'Alumnos',
        secondary=inscripcion,
        back_populates="cursos"
    )



