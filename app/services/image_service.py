# app/services/image_service.py
import json
from PIL import Image, ImageFilter, ImageDraw
import pandas as pd

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
    image.save("teste1.png")
    return image

def apply_size(image, gridSize):
    image = create_grid(image, gridSize)
    return image

def create_grid(image, gridSize):
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

def encontrar_cor_mais_proxima(cor):
    cores_disponiveis['Distancia'] = cores_disponiveis.apply(lambda row: ((cor[0]-row['Red'])**2 + (cor[1]-row['Green'])**2 + (cor[2]-row['Blue'])**2)**0.5, axis=1)
    cor_mais_proxima = cores_disponiveis.loc[cores_disponiveis['Distancia'].idxmin()]
    return (cor_mais_proxima['Red'], cor_mais_proxima['Green'], cor_mais_proxima['Blue']), cor_mais_proxima['Nome']


with open('app/static/utils/colors.json') as file:
    cores_disponiveis = json.load(file)
    cores_disponiveis = pd.DataFrame(cores_disponiveis)

def create_mosaic(image, gridSize, numberOfColors):
        # Carregar a imagem
        
    print("####################")
    print(image)
    print(gridSize)
    print(numberOfColors)
    print("####################")
    img = image
    img = img.resize((gridSize, gridSize))
    img.save("pixel.png")
    
    img_bkp = img

    # Obter as dimensões da imagem
    largura, altura = img.size

    # Inicializar um dicionário para armazenar as cores utilizadas e suas frequências
    cores_utilizadas = {}
    cores_utilizadas_filtrada = {}
    dados = []

    # Loop através de cada pixel da imagem
    for y in range(altura):
        for x in range(largura):
            cor = img.getpixel((x, y))
            cor_mais_proxima, nome_cor = encontrar_cor_mais_proxima(cor)
            img.putpixel((x, y), cor_mais_proxima)
            if nome_cor in cores_utilizadas:
                cores_utilizadas[nome_cor] += 1
            else:
                cores_utilizadas[nome_cor] = 1
                
            dados.append({"Largura": x, "Altura": y, "Cor": cores_utilizadas[nome_cor]})

    # Criar uma nova imagem com 10 pixels por linha e coluna
    new_img_10px = Image.new('RGB', (largura*10, altura*10))

    # Preencher a nova imagem com os pixels da imagem original
    for y in range(altura):
        for x in range(largura):
            cor = img.getpixel((x, y))
            for i in range(10):
                for j in range(10):
                    new_img_10px.putpixel((x*10+j, y*10+i), cor)

    new_img_10px.save("imagem_convertida_10px.png")

    # Salvar a nova imagem
    img.save("imagem_convertida.png")

    img = img.resize((gridSize, gridSize))
    # Ordenar as cores utilizadas em ordem decrescente
    cores_utilizadas_ordenadas = sorted(cores_utilizadas.items(), key=lambda x: x[1], reverse=True)

    # Selecionar as top 10 cores mais utilizadas
    top_10_cores = cores_utilizadas_ordenadas[:numberOfColors]

    # Criar uma nova imagem com as top 10 cores
    nova_img_top10 = Image.new('RGB', (largura*10, altura*10))
    
    # Filtrar o "cores_disponiveis" com apenas os resultados da "top_10_cores"
    cores_disponiveis_filtradas = cores_disponiveis[cores_disponiveis['Nome'].isin([cor[0] for cor in top_10_cores])]

    # Preencher a nova imagem com as top 10 cores
    for y in range(altura):
        for x in range(largura):
            cor = img_bkp.getpixel((x, y))
            cor_mais_proxima, nome_cor = encontrar_cor_mais_proxima(cor)
            if nome_cor in [cor[0] for cor in top_10_cores]:
                if nome_cor in cores_utilizadas_filtrada:
                    cores_utilizadas_filtrada[nome_cor] += 1
                else:
                    cores_utilizadas_filtrada[nome_cor] = 1
                
                dados.append({"Largura": x, "Altura": y, "Cor": cores_utilizadas[nome_cor]})
                
                for i in range(10):
                    for j in range(10):
                        nova_img_top10.putpixel((x*10+j, y*10+i), cor_mais_proxima)
    
    # Ordenar as cores utilizadas filtradas em ordem decrescente
    cores_utilizadas_filtrada_ordenadas = sorted(cores_utilizadas_filtrada.items(), key=lambda x: x[1], reverse=True)

    # Exibir a lista das cores utilizadas filtradas e suas frequências em ordem decrescente
    for cor, frequencia in cores_utilizadas_filtrada_ordenadas:
        print(cor, "-", frequencia)
    
    nova_img_top10.save("imagem_top10.png")
    
    
    # image = image.quantize(colors=numberOfColors)
    # image = image.resize((gridSize, gridSize), Image.NEAREST)
    # image = image.resize((original_width, original_height), Image.NEAREST)
    return nova_img_top10