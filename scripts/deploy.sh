#! /bin/bash 

# install required node modules for deployment:
npm install
npm install -g serverless

# deploy to every aws region:
export REGIONS=('ap-southeast-1' 'ap-southeast-2' 'us-east-1' 'us-east-2' 'us-west-1' 'us-west-2' 'ap-northeast-2' 'ap-south-1' 'ap-northeast-1' 'ca-central-1' 'eu-central-1' 'eu-west-1' 'eu-west-2' 'sa-east-1')

for REGION in $REGIONS
do
    echo "Deploying to region: ${REGION}"
    serverless deploy -v --region $REGION
done
