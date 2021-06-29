FROM python
RUN pip install Flask
RUN pip install flask-mysqldb
RUN pip install -U flask-cors
COPY . .
CMD ["python3", "/main.py"] 