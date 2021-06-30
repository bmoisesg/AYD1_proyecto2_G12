FROM python
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "/app.py"] 