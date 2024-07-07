FROM python:3
WORKDIR /opt/python_projects/apple_parser
COPY requirements.txt ./
COPY main.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./main.py" ]