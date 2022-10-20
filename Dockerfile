ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app
EXPOSE 8000