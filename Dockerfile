FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install --no-cache-dir -U pip \
    && python -m pip install --no-cache-dir \
      sibyl-memory-cli==0.3.17 \
      sibyl-memory-mcp==0.1.11

COPY scripts/ /app/scripts/

ENV SIBYL_MEMORY_DB=/data/memory.db

CMD ["sibyl-memory-mcp"]
