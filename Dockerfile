FROM python:3.10

RUN apt-get update && apt-get install -y netcat-openbsd

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . .

COPY run_migrations.sh /code/run_migrations.sh
RUN chmod +x /code/run_migrations.sh
ENTRYPOINT ["/code/run_migrations.sh"]