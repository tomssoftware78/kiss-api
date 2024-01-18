#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
COPY ./driver/intersystems_irispython-3.2.0-py3-none-any.whl /code/iris.whl

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install /code/iris.whl

#
COPY ./app /code/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
#If behind proxy
#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
