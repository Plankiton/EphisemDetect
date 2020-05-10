from os.path import join as pjoin
from ephisem_detect import *
from hashlib import sha1 as hash
from flask import (Flask,
                   redirect,
                   request,
                   render_template as render)
from web_interface.session import session

server = Flask('Ephisem Detect')
server.config['UPLOAD_FOLDER'] = 'images'

@server.route('/')
def index():
    return render('index.html')

@server.route('/send', methods = ['POST'])
def send():
    from datetime import datetime as d

    files = []
    for f in request.files.getlist('image'):
        timestamp = d.now().timestamp()
        hashname = hash(bytes(f.filename, 'utf-8')).hexdigest()
        filename = f'{timestamp}.{hashname}{f.filename[f.filename.rindex("."):]}'
        filedir = pjoin(
            server.config['UPLOAD_FOLDER'],
            filename
        )

        f.save(filedir)
        files.append({
            'dir': filedir,
            'filename': f.filename
        })

    session['ephisem.files'] = files
    return redirect('/analize')

@server.route('/analize', methods = ['GET'])
def analize():

    type_slice = 'middle'
    data = prepar_data(slices_dir = 'slices', type_slice = type_slice)
    files = session['ephisem.files']
    for f in range(len(files)):

        file = files[f]

        img = Image.open(file['dir'])
        img_map = compress_map(threshold(img))

        total = 0
        percentages = list(compair(data, img_map))
        for p in range(len(percentages)):
            total += percentages[p][0]

        files[f]['ephisem_level'] = total/len(percentages)
        files[f]['compair_percentes'] = total/len(percentages)

    return render('results.html', data = files)
