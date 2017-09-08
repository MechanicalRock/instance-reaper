''' the reaper module which contains the reaper class '''
from os import environ
import logging
from datetime import datetime, timedelta
from time import sleep
from dateutil.tz import tzutc
import boto3


class Reaper(object):
    ''' the reaper class, containing core functionality for instance-reaper '''

    FORMAT = '%(asctime)-15s instance-reaper: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    def __init__(self, region_name):
        self.cloudwatch_client = boto3.client(
            'cloudwatch', region_name=region_name)
        self.ec2_resource = boto3.resource('ec2', region_name=region_name)
        self.ec2_client = boto3.client('ec2', region_name=region_name)

        s3_endpoint = "http://localhost:4572" if self.is_local_env() else None
        self.s3_resource = boto3.resource('s3', endpoint_url=s3_endpoint)

        sns_endpoint = "http://localhost:4575" if self.is_local_env() else None
        self.sns_resource = boto3.resource('sns', endpoint_url=sns_endpoint)

    @staticmethod
    def is_local_env():
        ''' returns boolean, based whether the env variable is set '''
        return environ.get("ENV") == "local"

    @staticmethod
    def is_instance_mature(launch_time):
        ''' instance must be older than 3 hours '''
        now = datetime.utcnow()
        tz_now = datetime(now.year, now.month, now.day,
                          now.hour, now.minute, now.second, tzinfo=tzutc())
        age_in_hours = (tz_now - launch_time).total_seconds() / 3600
        return age_in_hours > 3

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

    def get_metric(self, instance_id, metric):
        ''' gets a metric from CloudWatch '''
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=3)

        return self.cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=10,
            Statistics=['Average']
        )

    @staticmethod
    def get_average_metric(datapoints):
        ''' calculates the average of all datapoints '''
        averages = [point['Average'] for point in datapoints]
        return reduce((lambda x, y: x + y), averages) / len(averages)

    def is_instance_idle(self, instance):
        ''' determines if an instance is idle and stops it, if it is idle '''
        instance_id = instance['InstanceId']

        if "Prod" in self.get_tags(instance):
            return False

        cpu_util = self.get_metric(instance_id, 'CPUUtilization')
        network_out = self.get_metric(instance_id, 'NetworkOut')

        average_cpu_util = self.get_average_metric(cpu_util['Datapoints'])
        average_net_out = self.get_average_metric(
            network_out['Datapoints']) / 1000000

        return self.stop_idle_instance(instance, average_cpu_util, average_net_out)

    def stop_idle_instance(self, instance, cpu_util, network_out):
        ''' stops an idle instance, returns true if the instance was stopped '''
        logging.info("CPU utilisation is %s", cpu_util)
        logging.info("Network out is %s", network_out)

        is_stopped = False

        if cpu_util < 2 and network_out < 5:
            logging.info("Stopping instance with id: %s",
                         instance['InstanceId'])
            is_stopped = self.stop_instance(instance)

        return is_stopped

    def stop_instance(self, instance):
        ''' stops the instance passed in as a parameter '''
        instance_id = instance['InstanceId']
        self.ec2_resource.instances.filter(InstanceIds=[instance_id]).stop()

        while instance['State']['Name'] != 'stopping':
            sleep(15)
            instance = self.ec2_client.describe_instances(InstanceIds=[instance_id])[
                'Reservations'][0]['Instances'][0]

        return instance['State']['Name'] == 'stopping'

    def is_instance_stopped(self, instance_id):
        ''' checks if a particular instance exists '''
        instance = self.ec2_client.describe_instances(InstanceIds=[instance_id])[
            'Reservations'][0]['Instances'][0]
        return instance['State']['Name'] == 'stopping'

    def filter_instances(self, instances):
        ''' returns a list of instances that are older than 3 hours '''
        return [instance for instance in instances if self.is_instance_mature(instance)]

    def get_relevant_instances(self):
        ''' gets all the "running" instances in a region that are older than 3 hours '''
        instance_state_filter = {
            'Name': 'instance-state-name',
            'Values': ['running']
        }

        all_instances = self.ec2_client.describe_instances(
            Filters=[instance_state_filter])
        return self.filter_instances(all_instances['Reservations'][0]['Instances'])

    def stop_all_relevant_instances(self):
        ''' get all relevant instances and stop the bastards'''
        for instance in self.get_relevant_instances():
            self.is_instance_idle(instance)

    @staticmethod
    def get_tags(instance):
        ''' gets the instance tags, returns an array of tags '''
        return [tag['Value'] for tag in instance['Tags']]
