FROM python:3.12-alpine

RUN addgroup -S challenge && adduser -S -G challenge challenge

WORKDIR /app
COPY src/ /app/
RUN chmod 0555 /app/server.py

USER challenge
EXPOSE 31337

ENTRYPOINT ["python3", "-u", "/app/server.py"]
