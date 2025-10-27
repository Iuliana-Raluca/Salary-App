# Imagine de bază Python
FROM python:3.12-slim

# Setare folder de lucru în container
WORKDIR /app

# Copiază tot codul local în container
COPY . /app

# Instalează pachetele Python
RUN pip install --no-cache-dir -r requirements.txt

# Expune portul Flask (default)
EXPOSE 5000

# Comandă de pornire a aplicației
CMD ["python", "app.py"]
