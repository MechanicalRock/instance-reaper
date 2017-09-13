#! /bin/bash 

export ENV=local

# install:
pip install --upgrade --user awscli pip
pip install -r ./requirements.txt

echo "Creating test resources on localstack"
./scripts/scaffold-environment.sh

# rate code
pylint src || true

# test:
pytest --spec
lettuce tests