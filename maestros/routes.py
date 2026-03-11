from . import maestros
from flask import render_template, request, redirect, url_for, flash
from models import db, Alumnos, Maestros, Curso, inscripcion
import forms


@maestros.route("/")
def inicio():
    return render_template("index.html")

@maestros.route("/alumnos")
def alumnos():
    lista = Alumnos.query.all()
    return render_template("alumnos.html", alumnos=lista)


@maestros.route("/nuevo_alumno", methods=["GET", "POST"])
def nuevo_alumno():
    form = forms.UserForm2()

    if request.method == "POST":
        if form.validate():
            nuevo = Alumnos(
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                email=form.email.data,
                telefono=form.telefono.data
            )

            db.session.add(nuevo)
            db.session.commit()
        return redirect(url_for("maestros.alumnos"))
           

    return render_template("RegistroAlum.html", form=form)


@maestros.route("/detalles/<int:id>")
def detalles(id):
    alumno = Alumnos.query.get_or_404(id)
    return render_template("detalles.html", alumno=alumno)

@maestros.route("/modificar/<int:id>", methods=["GET", "POST"])
def modificar(id):

    alumno = Alumnos.query.get_or_404(id)
    form = forms.UserForm2(obj=alumno)

    if form.validate_on_submit():

        alumno.nombre = form.nombre.data
        alumno.apellidos = form.apellidos.data
        alumno.email = form.email.data
        alumno.telefono = form.telefono.data

        db.session.commit()

        return redirect(url_for("maestros.alumnos"))

    return render_template("modificar.html", form=form, alumno=alumno)


@maestros.route("/eliminar/<int:id>", methods=["GET", "POST"])
def eliminar(id):
    alumno = Alumnos.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(alumno)
        db.session.commit()
        return redirect(url_for("maestros.alumnos"))

    return render_template("eliminar.html", alumno=alumno)


@maestros.route("/maestros")
def listado_maestros():
    lista = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", maestros=lista)

@maestros.route("/detalle_maestro/<int:matricula>")
def detalle_maestro(matricula):

    maestro = Maestros.query.get_or_404(matricula)

    return render_template(
        "maestros/detalle_maestro.html",
        maestro=maestro
    )

@maestros.route("/nuevo_maestro", methods=["GET", "POST"])
def nuevo_maestro():
    form = forms.UserForm2()

    if request.method == "POST":
        if form.validate():

            matricula = request.form.get("matricula")

            maestro_existente = Maestros.query.get(matricula)

            if maestro_existente:
                form.matricula.errors.append("La matrícula ya está registrada")
                return render_template("maestros/form_maestro.html", form=form)

            nuevo = Maestros(
                matricula=matricula,
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                email=form.email.data,
                especialidad=form.especialidad.data
            )

            db.session.add(nuevo)
            db.session.commit()


            return redirect(url_for("maestros.listado_maestros"))

    return render_template("maestros/form_maestro.html", form=form)


@maestros.route("/modificar_maestro/<int:matricula>", methods=["GET", "POST"])
def modificar_maestro(matricula):
    maestro = Maestros.query.get_or_404(matricula)
    form = forms.UserForm2(obj=maestro)

    if request.method == "POST":
        if form.validate():

            maestro.nombre = form.nombre.data
            maestro.apellidos = form.apellidos.data
            maestro.email = form.email.data
            maestro.especialidad = form.especialidad.data

            db.session.commit()

            return redirect(url_for("maestros.listado_maestros"))

    return render_template("maestros/modificar_maestro.html", form=form, maestro=maestro)


@maestros.route("/eliminar_maestro/<int:matricula>", methods=["GET", "POST"])
def eliminar_maestro(matricula):
    maestro = Maestros.query.get_or_404(matricula)

    if request.method == "POST":
        db.session.delete(maestro)
        db.session.commit()

        return redirect(url_for("maestros.listado_maestros"))

    return render_template("maestros/eliminar_maestro.html", maestro=maestro)

@maestros.route("/cursos")
def cursos():
    lista = Curso.query.all()
    return render_template("cursos/listado_cursos.html", cursos=lista)


