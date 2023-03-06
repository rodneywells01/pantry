FROM python:3.11.2-alpine3.17

WORKDIR /app

# Dependencies
COPY requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools wheel


RUN pip3 install -r requirements.txt

# Copy Structure
COPY api /app/api
COPY scripts /app/scripts
COPY .flaskenv /app

EXPOSE 5000
EXPOSE 8080


ENV FLASK_APP=api/main
ENV FLASK_ENV=development


# CMD scripts/run_server.sh
# CMD flask run --host=0.0.0.0 --port=8080
CMD python api/main.py
