FROM python:3.9

WORKDIR /opt/app

COPY . .

RUN pip install --upgrade pip  --no-cache-dir -r requirement.txt

EXPOSE 5000

# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["uwsgi", "app.ini"]