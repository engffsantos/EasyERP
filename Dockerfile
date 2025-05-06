# Dockerfile

# Imagem base com Python
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements/base.txt requirements/prod.txt ./requirements/
RUN pip install --upgrade pip && pip install -r requirements/prod.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta padrão
EXPOSE 5000

# Comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
