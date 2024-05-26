# app/services/image_service.py
from PIL import Image, ImageFilter, ImageDraw

def apply_filter(image, gridSize, resamplingMethod):
    resamplingMethods = {
        'NEAREST': Image.NEAREST,
        'BOX': Image.BOX,
        'BILINEAR': Image.BILINEAR,
        'HAMMING': Image.HAMMING,
        'BICUBIC': Image.BICUBIC,
        'LANCZOS': Image.LANCZOS
    }
    resamplingMethod = resamplingMethods[resamplingMethod]

    original_width, original_height = image.size
    image = image.resize((gridSize, gridSize), resamplingMethod)
    image = image.resize((original_width, original_height), Image.NEAREST)

    return image
    # draw = ImageDraw.Draw(image)
    # y_start = 0
    # y_end = image.height
    # step_size_x = int(image.width / gridSize)

    # for x in range(0, image.width, step_size_x):
    #     line = ((x, y_start), (x, y_end))
    #     draw.line(line, fill=128)

    # x_start = 0
    # x_end = image.width
    # step_size_y = int(image.height / gridSize)

    # for y in range(0, image.height, step_size_y):
    #     line = ((x_start, y), (x_end, y))
    #     draw.line(line, fill=128)

    # return image