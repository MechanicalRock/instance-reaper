''' module for the email service '''
from os import environ
import re
import boto3


class EmailService(object):
    ''' class for the email service '''

    EMAIL_REGEX = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def __init__(self):
        self.ses = boto3.client('ses', region_name='us-east-1')

    def is_email(self, candidate):
        ''' checks whether the owner tag is a valid email '''
        is_email = False
        if self.EMAIL_REGEX.match(candidate):
            is_email = True
        return is_email

    def send_email(self, instance_id, presigned_url):
        ''' sends an email to the recipient informing that their instance
         with the instance_id has been stopped '''
        email = self.build_email(instance_id, presigned_url)
        self.ses.send_email(
            Source=email['source'],
            Destination=email['destination'],
            Message=email['message']
        )

    def build_email(self, instance_id, presigned_url):
        ''' builds the dict to send as an email '''
        team_email = environ.get("TEAM_EMAIL")
        return {
            'source': team_email,
            'destination': {
                'ToAddresses': [team_email]
            },
            'message': {
                'Subject': {
                    'Data': 'Instance Reaped!',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': self.build_email_body(instance_id, presigned_url),
                        'Charset': 'UTF-8'
                    }
                }
            }
        }

    @staticmethod
    def build_email_body(instance_id, presigned_url):
        ''' builds the message body for an email '''
        return ('Hello {}, \n'
                'This email serves to inform you that the ec2 instance, with the instance id: {},'
                ' has been stopped by the instance reaper.\n'
                'You have been sent this email, as you are a member of the team, concerned with '
                ' the management of this instance.\n\n'
                'To view the logs, check out this link: {}\n\n'
                'Kind Regards,\n'
                'The Instance Reaper\n').format(
                    environ.get('TEAM_NAME'),
                    instance_id,
                    presigned_url
                )
