FROM python:3.10-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
COPY Pipfile /tmp/

RUN pip install pipenv && \
    cd /tmp && pipenv lock --requirements > requirements.txt && \
    python -m pip install -r requirements.txt

WORKDIR /src

RUN useradd appuser && chown -R appuser /src
USER appuser

CMD ["python", "mqttuya.py"]
