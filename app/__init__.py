# app/__init__.py
from flask import Flask
from .routes import home, image_processing

app = Flask(__name__)
app.register_blueprint(home.bp)
app.register_blueprint(image_processing.bp)