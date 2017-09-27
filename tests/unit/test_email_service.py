"""
Unit tests for the email service class
"""
from os import environ
from src.utils.email_service import EmailService

EMAIL_SERVICE = EmailService()
INSTANCE_ID = '12345'
PRESIGNED_URL = 'https://www.mechanicalrock.io'
REGION = 'ap-southeast-1'
VALUES = [INSTANCE_ID, PRESIGNED_URL, REGION]

environ['TEAM_NAME'] = 'mechanicalrock'
environ['TEAM_EMAIL'] = 'team@mechanicalrock.io'


def make_general_assertions(values, test_value):
    """
    assert the values are in the test value
    """
    for value in values:
        assert value in test_value


def test_is_email():
    """
    test the is email function
    """
    email = 'bryan.yu@mechanicalrock.io'
    is_email = EMAIL_SERVICE.is_email(email)
    assert is_email is True, email


def test_build_email_body():
    """
    test the build email body function
    """
    email_body = EMAIL_SERVICE.build_email_body(
        INSTANCE_ID, PRESIGNED_URL, REGION)

    assert environ.get('TEAM_NAME') in email_body
    assert 'Instance Reaper' in email_body
    make_general_assertions(VALUES, email_body)


def test_build_email():
    """
    test the build email function
    """
    team_email = environ.get('TEAM_EMAIL')
    email = EMAIL_SERVICE.build_email(INSTANCE_ID, PRESIGNED_URL, REGION)
    email_body_text = email['message']['Body']['Html']['Data']

    assert email['source'] == team_email
    assert team_email in email['destination']['ToAddresses']
    make_general_assertions(VALUES, email_body_text)


def test_send_email():
    """
    tests the send email
    """
    # EMAIL_SERVICE.send_email(INSTANCE_ID, PRESIGNED_URL, REGION)
    pass


def test_get_html_template():
    """
    tests the function that returns the html template
    """
    email_string = EMAIL_SERVICE.build_email_body(
        INSTANCE_ID, PRESIGNED_URL, REGION)

    assert isinstance(email_string, str)
    make_general_assertions(VALUES, email_string)
