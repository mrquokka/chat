FROM python:3.10
RUN mkdir -p /server/
COPY . /server/
RUN curl -fsSL https://deb.nodesource.com/setup_17.x | bash -
RUN apt-get install -y nodejs
WORKDIR /server/frontend
RUN npm i
RUN npm run build

WORKDIR /server/
RUN pip install -r requirements.txt
EXPOSE 8080
RUN ls -la
WORKDIR /server/
COPY main.py /server/
CMD ["python", "main.py"]
