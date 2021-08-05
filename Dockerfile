FROM python:3.7.6-buster

RUN pip --no-cache-dir install pandas==1.3.1 numpy==1.21.1 sklearn
    
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "app.py"]

