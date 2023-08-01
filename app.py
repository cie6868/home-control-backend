from database import db
from flask import Flask
from device import device
from mapping import mapping
import os

DB_FILENAME = 'mapping.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILENAME}'
app.register_blueprint(device, url_prefix = '/api/v1/device')
app.register_blueprint(mapping, url_prefix = '/api/v1/mapping')

db.init_app(app)

@app.route('/')
def index():
    return '<p>CIE Home Control Backend</p>'

if __name__ == '__main__':
    if not os.path.isfile(DB_FILENAME):
        with app.app_context():
            db.create_all()

    app.run('localhost', 6880, debug = True)
