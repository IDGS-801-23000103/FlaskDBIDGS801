from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SECRET_KEY'] = 'mi_clave_super_secreta'

db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/index")
def index():
    alumno = Alumnos.query.all()
    return render_template("index.html", alumno=alumno)


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    form = forms.UserForm2()

    if request.method == "POST":
        if form.validate():

            try:
                nuevo_alumno = Alumnos(
                   
                    nombre=form.nombre.data,
                    apaterno=form.apaterno.data,
                    email=form.email.data
                )

                db.session.add(nuevo_alumno)
                db.session.commit()

               
                return redirect(url_for("alumnos"))

            except Exception as e:
                db.session.rollback()
                flash(f"Error al registrar: {str(e)}", "danger")
        else:
            print("Errores del formulario:", form.errors)
            flash("Error en el formulario ⚠️", "danger")

    return render_template("alumnos.html", form=form)



@app.route("/detalles", methods=["GET"])
def detalles():

    id = request.args.get('id')

    if id:
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alum1:
            return render_template(
                'detalles.html',
                id=alum1.id,
                nombre=alum1.nombre,
                apaterno=alum1.apaterno,
                email=alum1.email
            )

    return redirect(url_for('index'))

@app.route("/modificar", methods=["GET", "POST"])
def modificar():

    id = request.args.get('id')

    if not id:
        return redirect(url_for('index'))

    alumno = Alumnos.query.get(id)

    if not alumno:
        return redirect(url_for('index'))

    form = forms.UserForm2(obj=alumno)

    if request.method == "POST" and form.validate():

        alumno.nombre = form.nombre.data
        alumno.apaterno = form.apaterno.data
        alumno.email = form.email.data

        db.session.commit()

        return redirect(url_for('index'))

    return render_template("modificar.html", form=form)


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():

    id = request.args.get('id')

    if not id:
        return redirect(url_for('index'))

    alumno = Alumnos.query.get(id)

    if not alumno:
        return redirect(url_for('index'))

    if request.method == "POST":
        db.session.delete(alumno)
        db.session.commit()
        flash("Alumno eliminado correctamente 🗑️", "success")
        return redirect(url_for('index'))

    return render_template("eliminar.html", alumno=alumno)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
