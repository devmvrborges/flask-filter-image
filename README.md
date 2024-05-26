# Projeto Image Service

Este projeto é um serviço de manipulação de imagens que permite redimensionar imagens e aplicar diferentes métodos de amostragem.

## Como usar

Para usar este serviço, você precisa passar uma imagem e o método de amostragem desejado. Os métodos de amostragem disponíveis são:

- NEAREST
- BOX
- BILINEAR
- HAMMING
- BICUBIC
- LANCZOS

Por exemplo:

```python
from PIL import Image
from image_service import resize_image

# Carregar a imagem
image = Image.open('path_to_your_image.png')

# Redimensionar a imagem
resized_image = resize_image(image, 'BICUBIC', 100)
