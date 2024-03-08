#
FROM python:3.9
RUN apt-get update
RUN apt-get install -y apt-utils build-essential gcc

ENV JAVA_FOLDER java-se-8u41-ri

ENV JVM_ROOT /usr/lib/jvm

ENV JAVA_PKG_NAME openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz
ENV JAVA_TAR_GZ_URL https://download.java.net/openjdk/jdk8u41/ri/$JAVA_PKG_NAME

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*    && \
    apt-get clean                                                               && \
    apt-get autoremove                                                          && \
    echo Downloading $JAVA_TAR_GZ_URL                                           && \
    wget -q $JAVA_TAR_GZ_URL                                                    && \
    tar -xvf $JAVA_PKG_NAME                                                     && \
    rm $JAVA_PKG_NAME                                                           && \
    mkdir -p /usr/lib/jvm                                                       && \
    mv ./$JAVA_FOLDER $JVM_ROOT                                                 && \
    update-alternatives --install /usr/bin/java java $JVM_ROOT/$JAVA_FOLDER/bin/java 1        && \
    update-alternatives --install /usr/bin/javac javac $JVM_ROOT/$JAVA_FOLDER/bin/javac 1     && \
    java -version
#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
COPY ./driver/intersystems_irispython-3.2.0-py3-none-any.whl /code/intersystems_irispython-3.2.0-py3-none-any.whl
COPY ./driver/CacheDB.jar /code/app/driver/CacheDB.jar

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install /code/intersystems_irispython-3.2.0-py3-none-any.whl

#
COPY ./app /code/app

WORKDIR /code/app

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
#If behind proxy
#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
