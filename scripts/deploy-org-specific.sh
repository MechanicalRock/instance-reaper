#!/bin/bash 

role=$1

sts_json=`aws sts assume-role --role-arn $role --duration-seconds 3600 --role-session-name datablaize-devops`
export AWS_ACCESS_KEY_ID=$(echo $sts_json | jq .Credentials.AccessKeyId | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $sts_json | jq .Credentials.SecretAccessKey | xargs)
export AWS_SESSION_TOKEN=$(echo $sts_json | jq .Credentials.SessionToken | xargs)

mv setup setup.cfg

./scripts/deploy.sh

mv setup.cfg setup