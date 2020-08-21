# Instance Reaper #

**A microservice that will cull all superfluous ec2 instances in your AWS account and emails a report on the instances it looked at.**   

Instance Reaper is a scheduled job, that will run every 3 hours and look for any running EC2 instances that do not have the substring 'prod' present, in any of the instance's tags. The application evaluates the CPU utilisation and network out metrics, retrieved from CloudWatch. If the CPU utilisation is below 2%, NetworkOut is below 20kb and the instance has been running for more than 3 hours, then the instance will be stopped. All evaluated instances' details are logged to region-specific logging files in an s3 bucket for the sole purpose of storing all instance-reaper logs. If an instance has been stopped, a presigned URL is generated for the s3 log file and emailed to a SES registered team email. The presigned URL, will be valid for 36 hours.

# Ensure you have the following on your machine:

- node 
- npm 
- python2.7
- pip
- configured aws credentials

# Also, ensure you have:

- AWS account
- Registered SES email in the us-east-1 region 

# You will need to edit the serverless.yml file:

Just change the TEAM_NAME & TEAM_EMAIL env variables.

```yaml
provider:
  name: aws
  runtime: python2.7
  environment: 
    TEAM_NAME: your.team.name.here
    TEAM_EMAIL: your.team.email@teamdomain.com
```

# To deploy to all lambda enabled regions on your AWS account

Run the following, in the project root directory:

```bash
./scripts/deploy.sh
```

If you would like to deploy the Instance Reaper to a specific account/organisation within your AWS account:

```bash
./scripts/deploy-org-specific.sh ${ROLE_ARN}
```
