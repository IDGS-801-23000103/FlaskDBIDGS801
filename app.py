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
    return render_template("index.html")



@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():
    form = forms.UserForm2()

    if form.validate_on_submit():
        # Crear nuevo alumno
        alumno = Alumnos(
            id=form.id.data,
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            email=form.email.data
        )

        db.session.add(alumno)
        db.session.commit()

        flash("Alumno guardado correctamente ✅")

        return redirect(url_for('alumnos'))

    return render_template('Alumnos.html', form=form)



with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
