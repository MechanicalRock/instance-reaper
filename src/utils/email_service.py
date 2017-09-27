''' module for the email service '''
from os import environ
from os.path import join, dirname
import re
import boto3

__author__ = 'Mechanical Rock'
__version__ = '0.0.1'


class EmailService(object):
    """
    Sends emails to team members, of instances that have
    been stopped, by the instance reaper
    """
    EMAIL_REGEX = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    def __init__(self):
        self.ses = boto3.client('ses', region_name='us-east-1')

    def is_email(self, candidate):
        """
        checks whether the owner tag is a valid email

        :type candidate: string
        :param candidate: owner's email

        :rtype: boolean
        :return: true if valid email
        """
        is_email = False
        if self.EMAIL_REGEX.match(candidate):
            is_email = True
        return is_email

    def send_email(self, instance_id, presigned_url, region):
        """
        sends an email to the recipient informing that their instance
        with the instance_id has been stopped.

        :type instance_id: string
        :param instance_id: the id of the instance that has been stopped

        :type presigned_url: string
        :param presigned_url: the generated presigned url to the log file
        with the details of the stopped instances
        """
        email = self.build_email(instance_id, presigned_url, region)
        self.ses.send_email(
            Source=email['source'],
            Destination=email['destination'],
            Message=email['message']
        )

    def build_email(self, instance_id, presigned_url, region):
        """
        builds the object to send as an email

        :type instance_id: string
        :param instance_id: the id of the instance that has been stopped

        :type presigned_url: string
        :param presigned_url: the generated presigned url to the log file

        :rtype: dict
        :return: the email object to be sent out
        """
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
                    'Html': {
                        'Data': self.build_email_body(instance_id, presigned_url, region),
                        'Charset': 'UTF-8'
                    }
                }
            }
        }

    @staticmethod
    def build_email_body(instance_id, presigned_url, region):
        """
        builds the message body for an email

        :type instance_id: string
        :param instance_id: the id of the instance that has been stopped

        :type presigned_url: string
        :param presigned_url: the generated presigned url to the log file

        :rtype: dict
        :return: the email message to be sent out to team members
        """
        html_file = join(dirname(dirname(__file__)),
                         'resources', 'template.html')
        html_file = open(html_file, 'r')
        email = html_file.read()
        email = email.replace('{{region}}', region)
        email = email.replace('{instanceId}', instance_id)
        return email.replace('{logLink}', presigned_url)
