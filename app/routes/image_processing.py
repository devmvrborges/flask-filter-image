from flask import Flask, render_template, request, jsonify, Blueprint, send_file
from PIL import Image
import io
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
    print(file)
    
    print(numberOfColors)
    
    image = Image.open(file.stream)
    # output_image = image_service.apply_interpolation(image, gridSize, resamplingMethod)
    output_image = image.convert('RGB') 
    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    # output_image.save('image2.png')
    mosaic_image = image_service.create_mosaic(output_image, 32, numberOfColors)
    
    # image = Image.open(file.stream)
    # image.save('image.jpg')
    # colors = int(request.form['colors'])
    # print(colors)
    # data = []
    # colors_avaiables = []
    # preview_content = unquote(request.form.get('previewContent'))
    # print(preview_content)
    
    # image_data = base64.b64decode(preview_content.split(',')[1])
    # Agora image_data contém os dados da imagem em bytes.
    # Você pode salvar a imagem em um arquivo assim:
    # with open('preview.png', 'wb') as f:
    #     f.write(image_data)
        
        
    # with open('app/static/utils/colors.json') as f:
    #     colors_avaiables = json.load(f)
    #     colors_avaiables = list(colors_avaiables)
        
    mosaic_image = mosaic_image.convert('RGB') 

    byte_arr = io.BytesIO()
    mosaic_image.save(byte_arr, format='PNG')
    byte_arr.seek(0)
    return send_file(byte_arr, mimetype='image/png')
    # print(colors_avaiables)
    
    # for i in colors_avaiables:
    #     hex_value = '#{:02x}{:02x}{:02x}'.format(*map(int, colors[i].get('color')[4:-1].split(',')))
    #     data.append({'name': colors[i].get('name'), 'color': hex_value, 'value': 100})
    #     print(i)
        
    # return mosaic_image