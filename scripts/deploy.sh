#! /bin/bash 

# install required node modules for deployment:
rm -rf node_modules
npm install --only=production
npm install -g serverless

# deploy to every lambda enabled aws region:
declare -a regions=('ap-southeast-1' 'ap-southeast-2' 'us-east-1' 'us-east-2' 'us-west-1' 'us-west-2' 'ap-northeast-2' 'ap-south-1' 'ap-northeast-1' 'ca-central-1' 'eu-central-1' 'eu-west-1' 'eu-west-2' 'sa-east-1')

for region in ${regions[@]}
do
    echo "Deploying to region: $region"
    serverless deploy -v --region $region
done
