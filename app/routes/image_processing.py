from flask import Flask, render_template, request, jsonify, Blueprint, send_file
from PIL import Image
import io
import pandas as pd
from ..services import image_service
import json
import os
from urllib.parse import unquote
import base64

bp = Blueprint('image_processing', __name__)

@bp.route('/apply_interpolation', methods=['POST'])
def apply_interpolation():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    gridSize = int(request.form['gridSize'])
    resamplingMethod = request.form['interpolation']
    print(gridSize, resamplingMethod)
    
    image = Image.open(file.stream)
    output_image = image_service.apply_interpolation(image, gridSize, resamplingMethod)
    output_image = output_image.convert('RGB')  # Convert image to RGB mode
    
    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return send_file(byte_arr, mimetype='image/png')


@bp.route('/apply_size', methods=['POST'])
def apply_size():
    print('apply_size')
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    gridSize = int(request.form['gridSize'])
    image = Image.open(file.stream)
    
    output_image = image_service.apply_size(image, gridSize)
    output_image = output_image.convert('RGB') 

    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return send_file(byte_arr, mimetype='image/png')


@bp.route('/get_colors', methods=['POST'])
def get_colors():
    
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    numberOfColors = int(request.form['colors'])
    gridSize = int(request.form['gridSize'])
    image = Image.open(file.stream)
    output_image = image.convert('RGB') 
    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    colors = []
    mosaic_image, colors = image_service.create_mosaic(output_image, gridSize, numberOfColors)
    data = []
        
    with open('app/static/utils/colors.json') as f:
        colors_avaiables = json.load(f)
        colors_avaiables = list(colors_avaiables)
        
    mosaic_image = mosaic_image.convert('RGB') 

    byte_arr = io.BytesIO()
    mosaic_image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    
    colors = pd.DataFrame(colors, columns=['Nome', 'Quantidade'])
    cores_disponiveis = pd.DataFrame(colors_avaiables)
    merged_df = pd.merge(colors, cores_disponiveis, on='Nome')
    
    for i in merged_df.iterrows():
        hex_value = '#{:02x}{:02x}{:02x}'.format(*map(int, i[1]['RAW'][4:-1].split(',')))
        data.append({'name': i[1]['Nome'], 'color': hex_value, 'value': i[1]['Quantidade']})

    image_bytes = byte_arr.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    response = {
        'image': image_base64,  # Convert the image to bytes
        'data': data  # JSON data
    }

    return jsonify(response)