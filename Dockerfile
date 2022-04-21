FROM python:3.10
RUN mkdir -p /server/
COPY . /server/
WORKDIR /server/
RUN pip install -r requirements.txt
EXPOSE 8080
RUN ls -la
WORKDIR /server/
COPY main.py /server/
CMD ["python", "main.py"]
