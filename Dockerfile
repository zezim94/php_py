# Usa imagem base com Python
FROM python:3.11

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta padrão do Flask
EXPOSE 5000

# Comando para rodar a aplicação com Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
