# Stage 1: builder
FROM python:3.12 AS builder

# Install uv binary from it's official docker repository
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install OS-level dependencies(needed for compiling python packages)
RUN apt-get update && apt-get install -y \
apt-utils curl build-essential gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /code-in-docker

COPY driver/ ./driver

# Copy dependency management files
COPY uv.lock .
COPY pyproject.toml .

RUN uv venv
# Activeer venv en installeer dependencies
RUN . .venv/bin/activate
RUN uv cache clean
RUN uv sync --frozen --compile-bytecode

# Stage 2: Runtime
FROM python:3.12 AS runtime

ENV JAVA_FOLDER=java-se-8u41-ri

ENV JVM_ROOT=/usr/lib/jvm

ENV JAVA_PKG_NAME=openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz
ENV JAVA_TAR_GZ_URL=https://download.java.net/openjdk/jdk8u41/ri/$JAVA_PKG_NAME

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

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set all environment variables in one command
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENV PATH="/code-in-docker/.venv/bin:$PATH"

WORKDIR /code-in-docker

#### Copy thevirtual environment from the builder stage
COPY --from=builder /code-in-docker /code-in-docker
COPY app/ .
COPY kiss_fc_api .

RUN mkdir -p /logs



CMD ["uv", "run", "gunicorn", "main:app", "--bind", "0.0.0.0:80", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "0"]