FROM python:3.12-slim

WORKDIR /app

# Copia os requisitos
COPY app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

# Copia o restante do código
COPY . .

# Altera de "api:app" para "app.api:app" (pasta.arquivo:variável)
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]