# Use official Python slim image
FROM python:3.11-slim


# Create app directory
WORKDIR /app


# system deps (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
libpq-dev \
&& rm -rf /var/lib/apt/lists/*


# copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# copy source
COPY ./app ./app


# create a non-root user (best practice)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser


# port
EXPOSE 80


# Start using Gunicorn + Uvicorn workers for concurrency
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:80", "--access-logfile", "-"]