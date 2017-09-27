# Instance Reaper #

**A microservice that will cull all superfluous ec2 instances in your AWS account and emails a report on the instances it looked at.**   

Instance Reaper is a scheduled job, that will run every 3 hours and look for any running ec2 instances that do not have the string 'prod' present, in any of the instance's tags. The instance CPU utilization and network out metrics are then retrieved from CloudWatch and evaluated. If the CPU Utilisation is below 2% and NetworkOut is below 5kb, then the instance will be stopped. All instance details are logged to a region-specific logging file in a global S3 bucket. A pre-signed URL is then generated for the report, with an expiry date of two days, and sent to a registered team email.

# Ensure you have the following on your machine:

- node 
- npm 
- python2.7
- pip
- configured aws credentials

# You will need to edit the serverless.yml file:

Just change the TEAM_NAME & TEAM_EMAIL env variables.

```yml
provider:
  name: aws
  runtime: python2.7
  environment: 
    TEAM_NAME: your.team.name.here
    TEAM_EMAIL: your.team.email@teamdomain.com
```

# To deploy to all lambda enabled regions on your AWS account

Run the following, in the project root directory:

> ./scripts/deploy.sh
