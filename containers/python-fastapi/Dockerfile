FROM python:3.9-alpine

WORKDIR /code

# Install ffmpeg
RUN apk add --no-cache ffmpeg

COPY ./containers/python-fastapi/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./containers/python-fastapi/app /code/app

EXPOSE 8081

CMD ["fastapi", "run", "app/main.py", "--port", "8081"]
