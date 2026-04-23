# Imagem base para rodar o robô
FROM python:3.9-slim

# Atualizar pacotes e instalar o Docker no container
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh \
    && rm -f get-docker.sh

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o script do robô e outros arquivos necessários para dentro do container
COPY run_robot.sh /app/
COPY requirements.txt /app/

# Instale as dependências Python, se necessário
RUN pip install --no-cache-dir -r requirements.txt

# Dê permissões de execução ao script
RUN chmod +x /app/run_robot.sh

# Comando que será executado quando o container for iniciado
CMD ["/app/run_robot.sh"]