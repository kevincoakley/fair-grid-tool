FROM python:3.9-slim
MAINTAINER Kevin Coakley <kcoakley@sdsc.edu>

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBUG=""
ARG SECRET_KEY=abc123

RUN mkdir /django

COPY . /django
WORKDIR /django

RUN pip install gunicorn
RUN pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py loaddata initial

RUN groupadd -g 999 django && \
    useradd -r -u 999 -g django django

RUN chown -R django:django /django

USER django

EXPOSE 8000

CMD gunicorn fgt.wsgi:application --bind 0.0.0.0:8000 --workers=4 --access-logfile '-' --error-logfile '-'