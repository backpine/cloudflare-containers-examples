FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

EXPOSE 8081

CMD ["fastapi", "run", "app/main.py", "--port", "8081"]
