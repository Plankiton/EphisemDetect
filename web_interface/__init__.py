from os.path import join as pjoin
from ephisem_detect import *
from hashlib import sha1 as hash
from flask import (Flask,
                   redirect,
                   request,
                   render_template as render)
from web_interface.session import session
from json import loads
rm = lambda d: system(f'rm "{d}"')

data = {}
with open('static/data.json') as json:
    data = loads(json.read())
server = Flask('Ephisem Detect')
server.config['UPLOAD_FOLDER'] = 'static/images'



@server.route('/')
def index():
    from os import listdir, system
    for f in listdir('static/images'):
        rm(f'static/images/{f}')
    return render('index.html')



@server.route('/send', methods = ['POST', 'GET'])
def send():
    if request.method == 'GET':
        return redirect('/')

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
            'filename': f.filename,
            'name': f.filename[:f.filename.index('.')]
        })

    session['ephisem.files'] = files
    return redirect('/loading?page=analize')



@server.route('/loading')
def loading():
    page = request.args.get('page', default='analize')
    return render('loading.html', page=page)



@server.route('/analize', methods = ['GET'])
def analize():
    files = {}
    try:
        files = session['ephisem.files']
    except KeyError:return redirect('/')
    for f in range(len(files)):
        file = files[f]

        img = Image.open(file['dir'])
        img_map = compress_map(threshold(img))

        total = 0
        slice_type = file['filename'][
            file['filename'].index('_')+1:file['filename'].index('.')
        ]
        percentages = list(compair(data[slice_type], img_map))
        for p in range(len(percentages)):
            total += percentages[p][0]

        files[f]['slice_type'] = slice_type
        files[f]['ephisem_level'] = total/len(percentages)
        files[f]['compair_percentages'] = percentages
    session.pop('ephisem.files')
    return render('results.html', data = files)
