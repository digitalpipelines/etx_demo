import os
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.password_validation import validate_password


class DemoTest(TestCase):

    def test_secret_key_strength(self):
        try:
            validate_password(settings.SECRET_KEY)
        except Exception as e:
            msg = f"Bad Secret Key {e.messages}"
            self.fail(msg)
        
