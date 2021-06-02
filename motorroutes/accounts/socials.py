from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """
    Google class to validate auth token and
    fetch the user info and return it
    """
    @staticmethod
    def validate(auth_token):
        """
        Query to google oauth2 api to fetch the user info
        """
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info

        except Exception as e:
            return "The token is either invalid or has expired"
