''' instance reaper lambda module '''
import boto3
from src.domain.reaper import Reaper


def reaper_event_handler(event, context):
    ''' instance reaper lambda handler '''
    region = boto3.session.Session().region_name
    reaper = Reaper(region_name=region)
    reaper.stop_all_relevant_instances()

    return {
        "message": "Removed all idle, non-'Prod' instances in the region {}".format(region),
        "event": event
    }
