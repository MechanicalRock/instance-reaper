''' module for the email service '''
from os import environ
from os.path import join, dirname
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
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

    def send_email(self, instance_id, region, log_file):
        """
        sends an email to the recipient informing that their instance
        with the instance_id has been stopped.

        :type instance_id: string
        :param instance_id: the id of the instance that has been stopped

        :type presigned_url: string
        :param presigned_url: the generated presigned url to the log file
        with the details of the stopped instances

        :type region: string
        :param region: the region the instance resides in.

        :type log_file: string
        :param log_file: the location of the log file
        """
        email = self.build_email(instance_id, region, log_file)
        self.ses.send_raw_email(
            RawMessage={'Data': email.as_string()},
            Source=email['From'],
            Destinations=[email['To']]
        )

    def build_email(self, instance_id, region, log_file):
        """
        builds the object to send as an email

        :type instance_id: string
        :param instance_id: the id of the instance that has been stopped

        :type region: string
        :param region: the region the instance resides in.

        :type log_file: string
        :param log_file: the location of the log file

        :rtype: dict
        :return: the email object to be sent out
        """
        email = MIMEMultipart()
        email['Subject'] = 'Instance Reaped!'
        email['From'] = environ.get('TEAM_EMAIL')
        email['To'] = environ.get('TEAM_EMAIL')

        email.preamble = 'Multipart message.\n'

        email_body = self.build_email_body(instance_id, region)
        part = MIMEText(email_body, 'html')
        email.attach(part)

        part = MIMEApplication(open(log_file, 'rb').read())
        part.add_header('Content-Disposition',
                        'attachment', filename='reaper.log')
        email.attach(part)

        return email

    @staticmethod
    def build_email_body(instance_id, region):
        """
        builds the message body for an email

        :type instance_id: string
        :param instance_id: the id of the instance that has been stopped

        :rtype: dict
        :return: the email message to be sent out to team members
        """
        html_file = join(dirname(dirname(__file__)),
                         'resources', 'template.html')
        html_file = open(html_file, 'r')
        email = html_file.read()
        email = email.replace('{{region}}', region)
        return email.replace('{instanceId}', instance_id)
