FROM python:alpine
WORKDIR /app
COPY /app/main.py /app
COPY /app/tests/test_main.py /app
COPY requirements.txt /app
RUN cd /app && pip install -r requirements.txt
EXPOSE 80
CMD ["python", "/app/main.py"]
