FROM python:3.11-alpine

EXPOSE 5000 

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["sh", "start.sh"]


