"""
logging service module
"""
from os import environ
from os.path import join, dirname
from datetime import datetime
import boto3

__author__ = 'Mechanical Rock'
__version__ = '0.0.1'


class LoggingService(object):
    """
    Logging service for instance reaper actions

    :type region: string
    :param region: the aws region
    """
    BUCKET_NAME = 'instance-reaper-{}-logging'.format(environ.get('TEAM_NAME'))

    def __init__(self, region):
        s3_endpoint = "http://localhost:4572" if self.is_local() else None
        self.s3_resource = boto3.resource('s3', endpoint_url=s3_endpoint)
        self.log_key = 'instance-reaper-{}.log'.format(region)
        self.log_file = self.get_local_log_name(self.log_key)
        self.region = region

        # ensure log file exists
        bucket = self.s3_resource.Bucket(self.BUCKET_NAME)
        log_exists = False
        for bucket_object in bucket.objects.all():
            if self.log_key == bucket_object.key:
                log_exists = True

        if not log_exists:
            self.s3_resource.Object(self.BUCKET_NAME, self.log_key).put()

    @staticmethod
    def is_local():
        """
        checks if we are in a local environment

        :rtype: boolean
        :return: whether the ENV environment variable is set to local
        """
        return environ.get("ENV") == "local"

    def get_log(self):
        """
        downloads the log file
        """
        self.s3_resource.Bucket(self.BUCKET_NAME).download_file(
            self.log_key, self.log_file)

    def write_log(self, message):
        """
        writes a log message to the log file in the s3 bucket
        """
        with open(self.log_file, "a") as reaper_log:
            reaper_log.write("{}: {}\n".format(datetime.utcnow(), message))

    def save_log(self):
        """
        saves the newly adapted log file
        """
        self.s3_resource.Bucket(self.BUCKET_NAME).upload_file(
            self.log_file, self.log_key)

    def log_instance_details(self, instance, cpu_util, net_out, tags):
        """
        log the instance details

        :type instance: dict
        :param instance: the instance details to be logged

        :type cpu_util: int
        :param cpu_util: average cpu utilisation over 3 hours

        :type net_out: int
        :param net_out: average network out in kb over 3 hours

        :type tags: list
        :param tags: the instance tags
        """
        self.write_log("********************************************")
        self.write_log("Evaluating instance with id: {}".format(
            instance['InstanceId']))
        self.write_log("Instance launched at: {}".format(
            instance['LaunchTime']))
        self.write_log("Instance has tags: {}".format(tags))
        self.write_log("CPU utilisation is {}%".format(cpu_util))
        self.write_log("Network out is {}kb".format(net_out))

    def get_local_log_name(self, log_key):
        """
        get a file name for log file that can be stored locally or
        on a lambda container.

        :type log_key: string
        :param log_key: the file name to be used

        :rtype: string
        :return: the relevant file name for the environment
        """
        dev_log = join(dirname(dirname(__file__)), 'tmp', log_key)
        lambda_log = '/tmp/{}'.format(log_key)

        return dev_log if self.is_local() else lambda_log
