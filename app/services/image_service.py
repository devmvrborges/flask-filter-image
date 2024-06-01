# app/services/image_service.py
from PIL import Image, ImageFilter, ImageDraw

def apply_interpolation(image, gridSize, resamplingMethod):
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
    image = create_grid(image, gridSize)
    return image

def apply_size(image, gridSize):
    image = create_grid(image, gridSize)
    return image

def create_grid(image, gridSize):
    image = image.resize((512, 512))
    draw = ImageDraw.Draw(image)
    y_start = 0
    y_end = image.height
    step_size_x = int(image.width / gridSize)

    for x in range(0, image.width, step_size_x):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=(0, 0, 0))

    x_start = 0
    x_end = image.width
    step_size_y = int(image.height / gridSize)

    for y in range(0, image.height, step_size_y):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=(0, 0, 0))

    border_width = 1
    border_color = (0, 0, 0)  # Black color

    # Bottom border
    draw.line([(0, image.height - border_width), (image.width, image.height - border_width)], fill=border_color, width=border_width)

    # Right border
    draw.line([(image.width - border_width, 0), (image.width - border_width, image.height)], fill=border_color, width=border_width)
    return image
