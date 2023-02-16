FROM python
COPY run.py /app/
COPY requirements.txt /app/
COPY mnst /app/mnst/
COPY clients/ /app/clients/
COPY output/ /app/output/
WORKDIR /app
RUN apt update && pip install -r requirements.txt