FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml ./
COPY analytics-api/src ./analytics-api/src
COPY fixtures ./fixtures
RUN pip install --no-cache-dir .

EXPOSE 8080 8081
