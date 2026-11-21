# Imagen de la aplicación (solo lo necesario para ejecutar, sin pruebas)
FROM python:3.12-slim
WORKDIR /app
COPY src/ ./src/
ENV PYTHONPATH=/app/src PYTHONUNBUFFERED=1
# Usuario sin privilegios: buena práctica de seguridad en contenedores
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/salud')"
CMD ["python", "-m", "inventario.api"]
