from flask import Blueprint, request, send_file
from PIL import Image
import io
from ..services import image_service

bp = Blueprint('image_processing', __name__)

@bp.route('/apply_filter', methods=['POST'])
def apply_filter():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    gridSize = int(request.form['gridSize'])
    resamplingMethod = request.form['resamplingMethod']
    image = Image.open(file.stream)
    output_image = image_service.apply_filter(image, gridSize, resamplingMethod)
    output_image = output_image.convert('RGB')  # Convert image to RGB
    byte_arr = io.BytesIO()
    output_image.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    return send_file(byte_arr, mimetype='image/jpeg')