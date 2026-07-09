FROM python:3.14-slim

WORKDIR /app

RUN apt update && \
    apt install -y ffmpeg 

COPY pyproject.toml .

COPY src/ ./src/

RUN pip install .

CMD ["python", "-m", "voice_converter"]