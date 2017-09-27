"""
Unit tests for the LoggingService class
"""
from os import environ
from src.utils.logging_service import LoggingService

environ['ENV'] = 'local'
environ['TEAM_NAME'] = 'mechanicalrock'
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


def test_get_presigned_url():
    """
    Tests the function that generates the presigned URL
    """
    environ['TEAM_NAME'] = 'mechanicalrock'
    presigned_url = LOGGING_SERVICE.get_presigned_url()
    # assert isinstance(presigned_url, str)


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
