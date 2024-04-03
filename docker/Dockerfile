FROM python:3.11.5-bullseye

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && \
  apt-get -y install \
    bash \
    curl \
    git \
    htop \
    python3-aiofiles \
    vim \
    openssl \
    libssl-dev \
  && apt-get clean


# Install poetry
RUN pip install --no-cache poetry==1.4.0
COPY pyproject.toml poetry.lock /app/
RUN cd /app && poetry config virtualenvs.create false && poetry install

COPY application/ .
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=TRUE

CMD ["gunicorn", "application.wsgi:application", "--bind", "0.0.0.0:8000"]
