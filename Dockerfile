FROM beevelop/nodejs-python:latest

RUN npm install -g serverless

WORKDIR /instance-reaper
COPY . /instance-reaper
RUN pip install --upgrade pip && pip install -r /instance-reaper/dev-dependencies/requirements.txt

ENTRYPOINT /scripts/scaffold-environment.sh ; /bin/bash