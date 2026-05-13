
FROM python:3.13

WORKDIR /docker

COPY . .

CMD ["python", "app.py"]