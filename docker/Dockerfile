FROM python:3.11-bullseye
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir -p /code/app
COPY ./app /code/app/
WORKDIR /code/app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--reload"]