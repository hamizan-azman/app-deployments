FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir paper-scraper@git+https://github.com/blackadad/paper-scraper.git

CMD ["python", "-c", "from chemcrow.agents import ChemCrow; print('ChemCrow ready')"]
