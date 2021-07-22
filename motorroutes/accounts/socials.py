from rest_framework.exceptions import AuthenticationFailed

import google_auth_oauthlib.flow
import base64
import json



class Google:
    """
    Google class to validate auth token and
    fetch the user info and return it
    """
    SCOPES = ['openid',
              'https://www.googleapis.com/auth/userinfo.email',
              'https://mail.google.com/',
              'https://www.googleapis.com/auth/userinfo.profile',
              ]
    REDIRECT_URI = 'http://localhost:8000/api/accounts/oauth/google/'
    CLIENT_SECRET_JSON_PATH = 'accounts/google_client_secret_public.json'

    @staticmethod
    def fetch_google_user_info(code):
        """
        Query to google oauth2 api to fetch the user info
        """
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            # for public use:
            Google.CLIENT_SECRET_JSON_PATH,

            # for test purposes only:
            #'accounts/google_client_secret.json',

            scopes=Google.SCOPES)

        flow.redirect_uri = 'http://localhost:8000/api/accounts/oauth/google/'

        try:
            flow.fetch_token(code=code)
            user_credentials = Google.credentials_to_dict(flow.credentials)
            id_credentials = Google.decode_id_token(user_credentials.get('id_token', None))
            id_credentials['access'] = user_credentials['token']
            id_credentials['refresh'] = user_credentials['refresh_token']

        except Exception as e:
            raise AuthenticationFailed('The token is either invalid or has expired')

        Google.validate_google_user_info(id_credentials)

        return id_credentials

    @staticmethod
    def get_authorization_url():
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            # for public use:
            Google.CLIENT_SECRET_JSON_PATH,

            # for test purposes only:
            #'accounts/google_client_secret.json',

            scopes=Google.SCOPES
        )
        flow.redirect_uri = 'http://localhost:8000/api/accounts/oauth/google/'

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')
        return authorization_url

    @staticmethod
    def credentials_to_dict(credentials):

        cred_dict = {'id_token': credentials.id_token,
                     'token': credentials.token,
                     'refresh_token': credentials.refresh_token,
                     'token_uri': credentials.token_uri,
                     'client_id': credentials.client_id,
                     'client_secret': credentials.client_secret,
                     'scopes': credentials.scopes}
        return cred_dict

    @staticmethod
    def decode_id_token(token):
        parts = token.split(".")
        if len(parts) != 3:
            raise Exception("Incorrect id token format")

        payload = parts[1]
        padded = payload + '=' * (4 - len(payload) % 4)
        decoded = base64.b64decode(padded)

        return json.loads(decoded)

    @staticmethod
    def validate_google_user_info(user_credentials):
        iss = user_credentials.get('iss', None)  # must be 'https://accounts.google.com'
        aud = user_credentials.get('aud', None)
        sub = user_credentials.get('sub', None)  # unique google user id
        email = user_credentials.get('email', None)

        if sub is None or aud is None or email is None or iss != 'https://accounts.google.com':
            raise AuthenticationFailed('Authentication failed. Try again.')



