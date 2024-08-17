FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["sh", "start.sh"]


