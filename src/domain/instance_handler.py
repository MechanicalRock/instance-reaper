''' module to handle all interactions with instances '''
import boto3
from src.utils.email_service import EmailService


class InstanceHandler(object):
    ''' class to handle all instance interactions '''

    RUNNING_FILTER = {
        'Name': 'instance-state-name',
        'Values': ['running']
    }

    def __init__(self, region_name):
        self.ec2_client = boto3.client('ec2', region_name=region_name)
        self.email = EmailService()

    def get_running_instances(self):
        ''' returns all running instances '''
        return self.ec2_client.describe_instances(Filters=[self.RUNNING_FILTER])['Reservations']

    def get_instance(self, instance_id):
        ''' returns a specific instance with the matching instance_id '''
        return self.ec2_client.describe_instances(InstanceIds=[instance_id])[
            'Reservations'][0]['Instances'][0]

    @staticmethod
    def get_tags(tags):
        ''' gets the instance tags, returns an array of tags '''
        return [tag['Value'] for tag in tags]

    @staticmethod
    def build_tags(stack_value):
        ''' returns a TagSpecifications JSON object for the ec2 meta data,
        used for testing '''
        return [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Stack',
                        'Value': stack_value
                    }
                ]
            }
        ]

    @staticmethod
    def build_filter_criteria(stack_value):
        ''' used only for testing '''
        return [
            {
                'Name': 'tag:Stack',
                'Values': [stack_value]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]

    def is_instance_stopped(self, instance_id):
        ''' checks if a particular instance exists '''
        instance = self.get_instance(instance_id)
        return instance['State']['Name'] == 'stopping'

    def get_owner_tag(self, tags):
        ''' return the owner of the instance, if the owner tag exists '''
        owner = None
        for tag in self.get_tags(tags):
            if self.email.is_email(tag):
                owner = tag
                break
        return owner
