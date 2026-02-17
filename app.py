from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SECRET_KEY'] = 'mi_clave_super_secreta'

db.init_app(app)
csrf = CSRFProtect(app)


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

                flash("Alumno registrado correctamente ✅", "success")

                # 🔥 limpiar formulario
                return redirect(url_for("alumnos"))

            except Exception as e:
                db.session.rollback()
                flash(f"Error al registrar: {str(e)}", "danger")
        else:
            print("Errores del formulario:", form.errors)
            flash("Error en el formulario ⚠️", "danger")

    return render_template("alumnos.html", form=form)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
