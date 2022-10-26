FROM python:3.9-slim

EXPOSE 8501

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc
COPY . .

CMD streamlit run ./app/main.py