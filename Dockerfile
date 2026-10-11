# ---- build stage ----
FROM python:3.12-slim AS build
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- runtime stage ----
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 APP_VERSION=dev
RUN useradd --create-home --uid 10001 appuser
WORKDIR /app
COPY --from=build /install /usr/local
COPY app/app.py .
USER 10001
EXPOSE 8080
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "2", "app:app"]
