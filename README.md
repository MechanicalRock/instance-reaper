# README #

This README will document the steps for running the Instance Reaper

# To Run the tests:

> lettuce tests

`fdsaflasdf`

See here for running lambdas periodically:

http://docs.aws.amazon.com/lambda/latest/dg/with-scheduled-events.html

# Bring up the development environment

- docker-compose build dev-env
- docker-compose up
- docker-compose run --rm dev-env

# If you install a new pip module, remember:

> pip freeze > requirements.txt

# Check code quality

> pylint ./*


# Check utilization metrics for an ec2 instance and output to json file
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --dimensions Name=InstanceId,Value=i-02eb595d1ea548b31 --metric-name CPUUtilization --start-time 2017-07-10 --end-time 2017-08-12 --period 3600 --region ap-southeast-2 --statistics Average > cpu_utilization.json