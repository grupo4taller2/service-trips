import firebase_admin
from firebase_admin import credentials, messaging
import os
import json

FB_TYPE  = os.environ["FB_TYPE_TR"]
FB_PROJECT_ID = os.environ["FB_PROJECT_ID_TR"]
FB_PRIVATE_KEY_ID = os.environ["FB_PRIVATE_KEY_ID_TR"]
FB_PRIVATE_KEY = os.environ["FB_PRIVATE_KEY_TR"].replace(r'\n', '\n')
FB_CLIENT_EMAIL = os.environ["FB_CLIENT_EMAIL_TR"]
FB_CLIENT_ID = os.environ["FB_CLIENT_ID_TR"] 
FB_AUTH_URI = os.environ["FB_AUTH_URI_TR"]
FB_TOKEN_URI = os.environ["FB_TOKEN_URI_TR"]
FB_AUTH_PROVIDER_CERT_URL = os.environ["FB_AUTH_PROVIDER_CERT_URL_TR"]
FB_CLIENT_CERT_URL = os.environ["FB_CLIENT_CERT_URL_TR"]


creds_dict = {
    "type": FB_TYPE,
    "project_id": FB_PROJECT_ID,
    "private_key_id": FB_PRIVATE_KEY_ID,
    "private_key": FB_PRIVATE_KEY,
    "client_email": FB_CLIENT_EMAIL,
    "client_id": FB_CLIENT_ID,
    "auth_uri": FB_AUTH_URI,
    "token_uri": FB_TOKEN_URI,
    "auth_provider_x509_cert_url": FB_AUTH_PROVIDER_CERT_URL,
    "client_x509_cert_url": FB_CLIENT_CERT_URL,
}

firebase_cred = credentials.Certificate(creds_dict)
firebase_app = firebase_admin.initialize_app(firebase_cred)