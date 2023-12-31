FROM python:3.10-slim-buster

#setting work dir
WORKDIR /usr/src/app

#env vars
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


# install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/list/*


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt


# copy project files
COPY . .

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]