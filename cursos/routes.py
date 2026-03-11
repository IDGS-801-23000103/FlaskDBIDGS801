from . import cursos
from flask import render_template, request, redirect, url_for, flash
from models import db, Curso, Maestros, Alumnos
from forms import InscripcionForm



@cursos.route("/cursos")
def listado_cursos():

    lista = Curso.query.all()

    return render_template(
        "cursos/listado_cursos.html",
        cursos=lista
    )


@cursos.route("/nuevo_curso", methods=["GET","POST"])
def nuevo_curso():

    maestros = Maestros.query.all()

    if request.method == "POST":

        nuevo = Curso(
            nombre=request.form.get("nombre"),
            maestro_id=request.form.get("maestro_id")
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for("cursos.listado_cursos"))

    return render_template(
        "cursos/nuevo_curso.html",
        maestros=maestros
    )


@cursos.route("/detalle_curso/<int:id>")
def detalle_curso(id):

    curso = Curso.query.get_or_404(id)

    alumnos = Alumnos.query.all()

    return render_template(
        "cursos/detalle_curso.html",
        curso=curso,
        alumnos=alumnos
    )


@cursos.route("/agregar_alumno/<int:curso_id>", methods=["POST"])
def agregar_alumno(curso_id):

    curso = Curso.query.get_or_404(curso_id)

    alumno_id = request.form.get("alumno_id")

    alumno = Alumnos.query.get(alumno_id)

    curso.alumnos.append(alumno)

    db.session.commit()

    return redirect(url_for("cursos.detalle_curso", id=curso_id))


@cursos.route("/modificar_curso/<int:id>", methods=["GET","POST"])
def modificar_curso(id):

    curso = Curso.query.get_or_404(id)

    maestros = Maestros.query.all()

    if request.method == "POST":

        curso.nombre = request.form.get("nombre")
        curso.maestro_id = request.form.get("maestro_id")

        db.session.commit()

        return redirect(url_for("cursos.listado_cursos"))

    return render_template(
        "cursos/modificar_curso.html",
        curso=curso,
        maestros=maestros
    )


@cursos.route("/eliminar_curso/<int:id>", methods=["GET","POST"])
def eliminar_curso(id):

    curso = Curso.query.get_or_404(id)

    if request.method == "POST":

        db.session.delete(curso)
        db.session.commit()

        return redirect(url_for("cursos.listado_cursos"))

    return render_template(
        "cursos/eliminar_curso.html",
        curso=curso
    )

@cursos.route("/inscribir/<int:id>", methods=["GET", "POST"])
def inscribir_alumno(id):

    curso = Curso.query.get_or_404(id)
    alumnos = Alumnos.query.all()
    form = InscripcionForm()

    mensaje = None

    if request.method == "POST":

        alumno_id = request.form.get("alumno_id")
        alumno = Alumnos.query.get(alumno_id)

        if alumno in curso.alumnos:
            mensaje = "Este alumno ya está inscrito en este curso"

        else:
            curso.alumnos.append(alumno)
            db.session.commit()

            return redirect(url_for("cursos.detalle_curso", id=id))

    return render_template(
        "cursos/inscribir_alumno.html",
        curso=curso,
        alumnos=alumnos,
        form=form,
        mensaje=mensaje
    )

@cursos.route("/quitar_alumno/<int:curso_id>/<int:alumno_id>")
def quitar_alumno(curso_id, alumno_id):

    curso = Curso.query.get_or_404(curso_id)
    alumno = Alumnos.query.get_or_404(alumno_id)

    curso.alumnos.remove(alumno)
    db.session.commit()

    return redirect(url_for("cursos.detalle_curso", id=curso_id))