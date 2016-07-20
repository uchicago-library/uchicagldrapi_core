from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

try:
    from uchicagoldrhrapi.api import bp as hr_bp
    app.register_blueprint(hr_bp)
except:
    pass
