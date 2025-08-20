FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SERVER_IP=${SERVER_IP}
ENV SERVER_PORT=${SERVER_PORT}

CMD ["sh", "-c", "uvicorn server:app --host $SERVER_IP --port $SERVER_PORT --reload"]
