"""
Unit tests for the LoggingService class
"""
from os import environ
from json import dumps
from src.utils.logging_service import LoggingService

environ['ENV'] = 'local'
environ['TEAM_NAME'] = 'company'
REGION = 'ap-southeast-1'
LOGGING_SERVICE = LoggingService(REGION)


def test_is_local():
    """
    test the is local function
    """
    is_local = LOGGING_SERVICE.is_local()
    assert is_local is True


def test_get_local_log_name():
    """
    test the get local log name functionality
    """
    log_key = 'instance-reaper-{}.log'.format(REGION)
    local_log = LOGGING_SERVICE.get_local_log_name(log_key)

    assert 'src' in local_log

    environ['ENV'] = 'cloud'
    local_log = LOGGING_SERVICE.get_local_log_name(log_key)

    assert 'src' not in local_log


def test_get_log_file():
    """
    Tests the get log function
    """
    LOGGING_SERVICE.get_log()


def test_save_log():
    """
    test the save log function
    """
    LOGGING_SERVICE.save_log()


def test_log_instance_details():
    """ 
    tests the write log functionality
    """
    # set intial parameter values for write log function
    instance = {
        'InstanceId': '666',
        'LaunchTime': 'now'
    }
    cpu_util = 1
    net_out = 5
    tags = [{
        'Name': 'foo',
        'Value': 'bar'
    }]
    params = [instance['InstanceId'],
              instance['LaunchTime'], cpu_util, net_out, tags]
    # invoke write log function
    LOGGING_SERVICE.log_instance_details(instance, 1, 5, tags)
    # open file that was written to
    with open(LOGGING_SERVICE.log_file, 'r') as log:
        # create a list of all the lines in the file
        log = log.readlines()
        for arg in params:
            # assert that each parameter passed in, has been written to the log.
            assert any(str(arg) in line for line in log) is True
