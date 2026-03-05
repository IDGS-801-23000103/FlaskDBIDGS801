from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from flask_migrate import Migrate
from maestros import maestros  
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SECRET_KEY'] = '1234567890'


db.init_app(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

app.register_blueprint(maestros)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)