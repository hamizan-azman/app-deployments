FROM python:3.8.18-slim

EXPOSE 8338 8339 8340

ARG skip_ds_deps=true
ARG skip_dev_deps=yes

RUN apt-get update && apt-get clean && apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    build-essential \
    pwgen \
    libffi-dev \
    sudo \
    git-core \
    libpq-dev \
    g++ unixodbc-dev \
    xmlsec1 \
    libssl-dev \
    default-libmysqlclient-dev \
    freetds-dev \
    libsasl2-dev \
    unzip \
    libsasl2-modules-gssapi-mit && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --uid 1000 deepbi

COPY ./vrequment.txt /app/vrequment.txt
WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

RUN pip install pip==20.2.4

RUN if [ "x$skip_dev_deps" = "x" ] ; then pip install -r requirements_dev.txt ; fi

RUN pip install -r vrequment.txt

# Fix python 3.8.18 import error
RUN sed -i 's/from importlib_resources import path/from importlib.resources import path/g' /usr/local/lib/python3.8/site-packages/saml2/sigver.py && \
    sed -i 's/from importlib_resources import path/from importlib.resources import path/g' /usr/local/lib/python3.8/site-packages/saml2/xml/schema/__init__.py

COPY . /app

RUN chown -R deepbi:deepbi /app

USER deepbi

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8338/ || exit 1

ENTRYPOINT ["/app/bin/docker-entrypoint"]
CMD ["server"]
