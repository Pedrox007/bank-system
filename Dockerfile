FROM python:3.10

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

RUN mkdir /bank-system

WORKDIR /bank-system

COPY . /bank-system/

RUN pip install pipenv

RUN pipenv install

CMD ["manage.py", "runserver", "0.0.0.0:8080"]
