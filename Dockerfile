FROM python:3.10

ADD requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

WORKDIR /code

ADD . .
RUN ./setup.py sdist bdist_wheel && \
    ./setup.py install