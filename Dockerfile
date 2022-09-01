FROM python:3.10

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /src/requirements.txt

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /src/requirements.txt
RUN rm -rf /root/.cache/pip

# copy project
COPY . /src

CMD [ "python3", "main.py" ]