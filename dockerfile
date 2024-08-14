FROM python:3

WORKDIR /app

COPY . .

RUN pip install flask
RUN pip install flask_cors
RUN pip install requests
RUN pip install bs4

EXPOSE 81

CMD python scrapingServer.py