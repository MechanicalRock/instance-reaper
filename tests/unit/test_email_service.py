''' Module to test the functionality of the email service '''
from src.utils.email_service import EmailService


def test_is_email():
    ''' tests the is_email function '''
    email = 'bryan.yu@mechanicalrock.io'
    is_email = EmailService().is_email(email)
    assert is_email is True, email
