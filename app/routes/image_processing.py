from flask import Blueprint, request, send_file
from PIL import Image
import io
from ..services import image_service

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
    output_image = output_image.convert('CMYK') 
    
    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    
    return send_file(byte_arr, mimetype='image/jpeg')


@bp.route('/apply_size', methods=['POST'])
def apply_size():
    print('apply_size')
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    gridSize = int(request.form['gridSize'])
    image = Image.open(file.stream)
    
    output_image = image_service.apply_size(image, gridSize)
    output_image = output_image.convert('CMYK') 

    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    return send_file(byte_arr, mimetype='image/jpeg')