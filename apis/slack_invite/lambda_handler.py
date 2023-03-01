import json
import base64
import logging

import boto3
import os
import uuid
import botocore
import imghdr

import requests

logger = logging.getLogger(__name__)

ssm_client = boto3.client('ssm')
SLACK_ADMIN_TOKEN = ssm_client.get_parameters(Names=['/pythonwa/slack/admin_token']),

# add your token here, generate from https://api.slack.com/custom-integrations/legacy-tokens
# add all IDs of the channels you will want the users to be added automatically to
# you can get a list of your channels at https: // api.slack.com/methods/conversations.list
# http -v GET https://slack.com/api/conversations.list Authorization:"Bearer xoxp-123456-123456-123456"
CHANNELS = [
    'C1CD87S83',  # general
    'C1CEKD0JU',  # random
]


def invite_email(email: str) -> dict:
    """
    invite an email address to our slack

        https: // slack.com/api/users.admin.invite

        Argument	Example	Required	Description
        token	xxxx-xxxxxxxxx-xxxx	Required	Authentication token(Requires scope: 'client')
        email	john.doe@email.com	Required	Email address of the new user
        channels	C1234567890, G12345678	Optional	Comma-separated list of IDs(not names!) for channels, which the new user will auto-join. Both channel IDs for public channels and group IDs for private chanels work.
        first_name	John	Optional	Prefilled input for the "First name" field on the "new user registration" page.
        last_name	Doe	Optional	Prefilled input for the "Last name" field on the "new user registration" page.
        resend	true	Optional	Resend the invitation email if the user has already been invited and the email was sent some time ago.
        restricted	true	Optional	Invite a guest that can use multiple channels
        ultra_restricted	true	Optional	Invite a guest that can use one channel only
        expiration_ts	1510863690	Optional	Set the expiration timestamp for when the guest account will automatically be disabled
    """
    url = "https://slack.com/api/users.admin.invite"
    payload = {
        "token": SLACK_ADMIN_TOKEN,
        "email": email,
        "channels": ','.join(CHANNELS)
    }
    r = requests.get(url, params=payload)
    return r.json()


def handler(event, context):
    logger.info(event)
    # Generate random image id
    # image_id = str(uuid.uuid4())

    data: dict = json.loads(event["body"])
    email: str = data['email']
    # userid = data["userid"]
    # img = base64.b64decode(data["photo"])

    response: dict = invite_email(email)
    logger.info(response)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(response),
    }
