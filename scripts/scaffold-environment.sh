#!/bin/bash

COMPANY_NAME=$1
REGION=$2

# create localstack resources
if [ $ENV = "local" ]; then
    aws --endpoint-url=http://localhost:4572 s3 mb s3://instance-reaper-${COMPANY_NAME}-logging
else
    aws s3 mb s3://instance-reaper-${COMPANY_NAME}-logging --region ${REGION}
fi