from web import app
from flask import request

@app.errorhandler(404)
def page_not_found(e):
    return f"{request.path} not exist", 404

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"