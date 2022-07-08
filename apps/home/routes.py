# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask_login import login_required
from jinja2 import TemplateNotFound

# -*- coding: utf-8 -*-
from flask import Flask, request, make_response, render_template, url_for, g, send_from_directory, jsonify, send_file
from flask_restful import Resource, Api
from json import dumps
from loguru import logger
import yaml, uuid, base64, os, io
import pytesseract
import cv2
import subprocess
from subprocess import Popen
import time

try:
    from PIL import Image
except ImportError:
    import Image


# Validating file extention
def allowed_file(image_file):
    logger.info("Validating file extention")
    return '.' in image_file and \
           image_file.rsplit('.', 1)[1].lower() in "png,jpg,pdf,tiff"

# Getting file extention
def getExtention(image_file):
    logger.info("Getting file extention")
    filename, file_extension = os.path.splitext(image_file)
    return filename, file_extension

def convert_to_tiff(image_file):
    logger.info("Converting pdf to tiff")
    converted_file_name = image_file.replace('pdf','tiff')
    p = subprocess.Popen('convert -density 300 '+ image_file +' -background white -alpha Off '+ converted_file_name , stderr=subprocess.STDOUT, shell=True)
    p_status = p.wait()
    time.sleep(5)
    if os.path.exists(image_file):
        os.remove(image_file)
    return converted_file_name


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/ocr')
@login_required
def ocr():

    return render_template('home/ocr.html', segment='ocr')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
