''' module to handle interactions with cloudwatch '''
from datetime import datetime, timedelta
import boto3


class CloudwatchHelper(object):
    ''' class to handle all interactions with cloudwatch '''

    def __init__(self, region_name):
        self.client = boto3.client('cloudwatch', region_name=region_name)

    def get_metric(self, instance_id, metric):
        ''' gets a metric from CloudWatch '''
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=3)

        return self.client.get_metric_statistics(
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
        )['Datapoints']

    @staticmethod
    def get_metric_average(datapoints):
        ''' calculates the average of all datapoints '''
        averages = [point['Average'] for point in datapoints]
        return reduce((lambda x, y: x + y), averages) / len(averages)

    def get_average_metrics(self, instance_id):
        ''' builds a dict with the average for each relevant metric over the past 3 hours '''
        cpu_util = self.get_metric(instance_id, 'CPUUtilization')
        network_out = self.get_metric(instance_id, 'NetworkOut')
        return {
            'AvgCPUUtilisation': self.get_metric_average(cpu_util),
            'AvgNetworkOut': self.get_metric_average(network_out) / 1000
        }
