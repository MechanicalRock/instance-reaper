#!/bin/bash

company_name=mechanicalrock

# create localstack resources
if [ $ENV = 'local']; then
    aws --endpoint-url=http://localhost:4572 s3 mb s3://instance-reaper-${company_name}-logging
    aws --endpoint-url=http://locahost:4575 sns create-topic --name instance-reaper-notifications
else
    aws s3 mb s3://instance-reaper-${company_name}-logging
    aws sns create-topic --name instance-reaper-notifications
fi