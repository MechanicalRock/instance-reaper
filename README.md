# README #

# Ensure you have the following on your machine:

- node 
- npm 
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
