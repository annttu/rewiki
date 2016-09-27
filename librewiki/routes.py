# encoding: utf-8

from librewiki.app import app
import os
from flask import jsonify, request
import subprocess
from datetime import datetime


PREFIX = os.path.normpath(os.path.join(os.path.dirname(__file__), "../files"))
GIT = "/usr/bin/git"


def get_dir_path(path):
    return os.path.join(PREFIX, path)


def get_page_path(path):
    path = os.path.normpath(os.path.join(PREFIX, path, 'page.md'))
    common_prefix = os.path.commonprefix([path, PREFIX])
    if len(common_prefix) < len(PREFIX):
        raise Exception("Invalid Path %s" % PREFIX)
    return path


def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, 0o0700)


def sanitize_path(path):
    return path.replace("../", "")


@app.route('/')
def index():
    fd = open(os.path.join(os.path.dirname(__file__), "../static/index.html"))
    content = fd.read()
    fd.close()
    return content


@app.route('/content/<path:path>', methods=['GET', 'POST'])
def callback_path(path):
    path = sanitize_path(path)
    dirpath = get_dir_path(path)
    filepath = get_page_path(path)
    if request.method == 'POST':
        create_dir(dirpath)
        fd = open(filepath, 'w')
        fd.write(request.json['content'])
        fd.close()
        subprocess.call([GIT, '-C', PREFIX, 'add', filepath])
        subprocess.call([GIT, '-C', PREFIX, 'commit', "-m", 'Commit from web ui %s' % datetime.now().strftime("%d.%m.%Y %H:%M:%S")])
        return jsonify({'status': 'OK'}), 200
    else:
        data = {}
        if os.path.isfile(filepath):
            fd = open(filepath)
            data['content'] = fd.read()
            fd.close()
        data['directory'] = '%s' % dirpath
        data['path'] = path
        return jsonify(data)


@app.route('/content/<path:path>/_content')
def callback_path_content(path):
    path = sanitize_path(path)
    filepath = get_page_path(path)
    print(filepath)
    data = None
    if os.path.isfile(filepath):
        fd = open(filepath)
        data = fd.read()
        fd.close()
    else:
        return "", 404
    return data