FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# NÃO executar collectstatic aqui!
# Será executado no comando de start
#teste
# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn pallet_controller.wsgi --bind 0.0.0.0:8000"]