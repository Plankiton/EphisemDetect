from flask import (Flask,
    render_template as render)

server = Flask('Ephisem Detect')


@server.route('/')
def index():
    return render('index.html')

@server.route('/send', methods = ['POST'])
def send():
    pass
