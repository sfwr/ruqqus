FROM python:3.7-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "ruqqus.__main__:app", "-w", "3", "-k", "gevent", "--worker-connections", "6", "--preload", "--max-requests", "10000", "--max-requests-jitter", "500", "--reload", "-b", "0.0.0.0:8000"]