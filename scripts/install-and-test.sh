#! /bin/bash 

export ENV=local
export TEAM_NAME=team.name
export TEAM_EMAIL=team@email.co

# install:
pip install --upgrade --user awscli pip
pip install -r ./requirements.txt

echo "Creating test resources on localstack"
./scripts/scaffold-environment.sh

# rate code
pylint src tests/unit || true

# test:
pytest --spec
lettuce tests