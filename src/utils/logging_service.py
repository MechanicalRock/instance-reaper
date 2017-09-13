''' module for the logging service '''
from os import environ
from os.path import join, dirname
from datetime import datetime
import boto3


class LoggingService(object):
    ''' class for the logging service '''
    BUCKET_NAME = 'instance-reaper-{}-logging'.format(environ.get('TEAM_NAME'))

    def __init__(self, region):
        s3_endpoint = "http://localhost:4572" if self.is_local() else None
        self.s3_resource = boto3.resource('s3', endpoint_url=s3_endpoint)
        self.log_key = 'instance-reaper-{}.log'.format(region)
        self.log_file = self.get_local_log_name(self.log_key)

        # ensure log file exists
        bucket = self.s3_resource.Bucket(self.BUCKET_NAME)
        if self.log_key not in bucket.objects.all():
            self.s3_resource.Object(self.BUCKET_NAME, self.log_key).put()

    @staticmethod
    def is_local():
        ''' checks if we are in a local environment '''
        return environ.get("ENV") == "local"

    def get_log(self):
        ''' downloads the log file '''
        self.s3_resource.Bucket(self.BUCKET_NAME).download_file(
            self.log_key, self.log_file)

    def write_log(self, message):
        ''' writes a log message to the log file in the s3 bucket '''
        with open(self.log_file, "a") as reaper_log:
            reaper_log.write("{}: {}\n".format(datetime.utcnow(), message))

    def save_log(self):
        ''' saves the newly adapted log file '''
        self.s3_resource.Object(
            self.BUCKET_NAME, self.log_key).upload_file(self.log_file)

    def log_instance_details(self, instance, cpu_util, net_out, tags):
        ''' log the instance details '''
        self.write_log("********************************************")
        self.write_log("Evaluating instance with id: {}".format(
            instance['InstanceId']))
        self.write_log("Instance launched at: {}".format(
            instance['LaunchTime']))
        self.write_log("Instance has tags: {}".format(tags))
        self.write_log("CPU utilisation is {}%".format(cpu_util))
        self.write_log("Network out is {}kb".format(net_out))

    def get_local_log_name(self, log_key):
        ''' returns a name that can be stored locally '''
        dev_log = join(dirname(dirname(__file__)), 'tmp', log_key)
        lambda_log = '/tmp/{}'.format(log_key)

        return dev_log if self.is_local() else lambda_log

    def get_presigned_url(self):
        ''' creates and returns a presigned url for accessing the log file '''
        return boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.BUCKET_NAME,
                'Key': self.log_key
            },
            ExpiresIn=172800
        )
