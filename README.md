# Flask Filter Bricks

## Descrição
Este projeto é uma aplicação web desenvolvida em Flask e permite criar mosaicos a partir de uma foto, utilizando peças de Lego existentes no mercado. O processo envolve a filtragem e pesquisa das informações das peças de Lego disponíveis, para encontrar as peças mais adequadas para compor o mosaico.

## Como funciona
1. Carregue a foto desejada na aplicação utilizando uma biblioteca JavaScript.
2. Utilize a biblioteca JavaScript para selecionar a parte da foto que deseja ser exibida.
3. Selecione o tamanho do quadro, podendo ser 32x32 ou 64x64.
4. Selecione o algoritmo de processamento de imagem desejado para segmentar a foto em regiões.
5. Selecione a quantidade de cores que deseja utilizar.
6. Para cada região, utilize as funcionalidades de filtragem e pesquisa para encontrar as peças de Lego mais adequadas.
7. Monte o mosaico utilizando as peças selecionadas.
8. Exiba o mosaico final, incluindo a imagem original e a representação em peças de Lego.

## Requisitos adicionais
Além das funcionalidades já mencionadas, este projeto também requer:
- Algoritmo de processamento de imagem para segmentação da foto.
- As informações sobre as peças de Lego disponíveis no mercado, armazenado em um arquivo JSON na pasta `/static/utils/colors.json`.
- Lógica para calcular a melhor combinação de peças para cada região da foto.

## Executando o projeto

Para executar este projeto no seu computador, siga os passos abaixo:

1. Certifique-se de ter o Python instalado no seu computador. Você pode baixar a versão mais recente do Python em [python.org](https://www.python.org/downloads/).

2. Clone este repositório para o seu computador utilizando o seguinte comando no terminal:

    ```bash
    git clone https://github.com/seu-usuario/lego-bricks.git
    ```

    Certifique-se de substituir `seu-usuario` pelo seu nome de usuário do GitHub.

3. Navegue até o diretório do projeto:

    ```bash
    cd lego-bricks/flask-filter-bricks
    ```

4. Crie um ambiente virtual para o projeto. Execute o seguinte comando no terminal:

    ```bash
    python -m venv venv
    ```

5. Ative o ambiente virtual. No Windows, execute o seguinte comando:

    ```bash
    venv\Scripts\activate
    ```

    No macOS e Linux, execute o seguinte comando:

    ```bash
    source venv/bin/activate
    ```

6. Instale as dependências do projeto. Execute o seguinte comando:

    ```bash
    pip install -r requirements.txt
    ```

7. Inicie o servidor Flask. Execute o seguinte comando:

    ```bash
    flask run
    ```

8. Abra o seu navegador e acesse `http://localhost:5000` para visualizar a aplicação.

Agora você pode utilizar a aplicação Flask Filter Bricks no seu computador.

## Contribuição
Se você quiser contribuir para este projeto, siga as etapas abaixo:

1. Faça um fork do repositório
2. Crie uma branch para a sua feature: `git checkout -b minha-feature`
3. Faça as alterações necessárias e adicione os arquivos modificados: `git add .`
4. Faça o commit das suas alterações: `git commit -m "Minha feature"`
5. Faça o push para o repositório remoto: `git push origin minha-feature`
6. Abra um pull request no GitHub

## Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).