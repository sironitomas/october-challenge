FROM python:3.8-alpine
ENV FLASK_APP hello.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY hello.py hello.py
CMD ["flask", "run"]
