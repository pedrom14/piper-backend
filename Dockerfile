FROM ubuntu:22.04

# Instalar dependências básicas
RUN apt update && apt install -y python3 python3-pip curl

# Instalar o onnxruntime (opcional, para caso o piper precise)
RUN pip3 install flask

# Copiar arquivos do projeto
WORKDIR /app
COPY . .

# Dar permissão de execução ao binário do Piper
RUN chmod +x piper

# Expor a porta da API Flask
EXPOSE 5000

CMD ["python3", "app.py"]

