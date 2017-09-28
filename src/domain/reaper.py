''' the reaper module which contains the reaper class '''
from datetime import datetime
from time import sleep
import boto3
from dateutil.tz import tzutc
from src.domain.instance_handler import InstanceHandler
from src.domain.cloudwatch_helper import CloudwatchHelper
from src.utils.logging_service import LoggingService
from src.utils.email_service import EmailService


class Reaper(object):
    ''' the reaper class, containing core functionality for instance-reaper '''

    def __init__(self, region_name):
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)
        self.instance_handler = InstanceHandler(region_name)
        self.cloudwatch = CloudwatchHelper(region_name)
        self.email = EmailService()
        self.log = LoggingService(region_name)
        self.log.get_log()
        self.region = region_name

    def stop_all_relevant_instances(self):
        ''' get all relevant instances and stop the bastards'''
        instances = self.get_relevant_instances()
        for instance in instances:
            if self.is_instance_idle(instance):
                if self.stop_idle_instance(instance):
                    self.email.send_email(
                        instance['InstanceId'], self.region, self.log.log_file)
        self.log.save_log()

    def is_instance_idle(self, instance):
        ''' determines if an instance is idle and stops it, if it is idle '''
        metrics = self.cloudwatch.get_average_metrics(instance['InstanceId'])
        cpu_util = metrics['AvgCPUUtilisation']
        net_out = metrics['AvgNetworkOut']
        tags = self.instance_handler.get_tags(instance['Tags'])
        self.log.log_instance_details(instance, cpu_util, net_out, tags)
        return cpu_util < 2 and net_out < 5

    def get_relevant_instances(self):
        ''' gets all the "running" instances in a region that are older than 3 hours '''
        running_instances = self.instance_handler.get_running_instances()
        return self.filter_instances(running_instances)

    def stop_idle_instance(self, instance):
        ''' stops the instance passed in as a parameter '''
        instance_id = instance['InstanceId']
        self.log.write_log("Stopping instance with id: {}".format(instance_id))
        self.ec2_resource.instances.filter(InstanceIds=[instance_id]).stop()

        while instance['State']['Name'] != 'stopping':
            sleep(1)
            instance = self.instance_handler.get_instance(instance_id)

        return instance['State']['Name'] == 'stopping'

    def filter_instances(self, instances):
        ''' filter out prod instances and instances that are not old enough '''
        return [instance['Instances'][0] for instance in instances
                if self.instance_filter(instance)]

    def instance_filter(self, instance):
        ''' perform the necessary checks on the tags and age of the instance '''
        instance = instance['Instances'][0]
        instance_mature = self.is_instance_mature(instance['LaunchTime'])
        tags = self.instance_handler.get_tags(instance['Tags'])
        return instance_mature and not self.is_prod_instance(tags)

    @staticmethod
    def is_prod_instance(tags):
        ''' checks to see if the word prod is in any of the instance's tags '''
        return any('PROD' in tag.upper() for tag in tags)

    @staticmethod
    def is_instance_mature(launch_time):
        ''' instance must be older than 3 hours '''
        now = datetime.utcnow()
        tz_now = datetime(now.year, now.month, now.day,
                          now.hour, now.minute, now.second, tzinfo=tzutc())
        age_in_hours = (tz_now - launch_time).total_seconds() / 3600
        return age_in_hours > 3
