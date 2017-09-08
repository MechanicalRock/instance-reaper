#! /bin/bash 

export ENV=local

# install:
pip install --upgrade --user awscli pip
pip install -r ./requirements.txt

echo "Creating test resources on localstack"
sh ./scaffld-environment.sh

# test:
# pytest --spec
lettuce tests
pylint src || true