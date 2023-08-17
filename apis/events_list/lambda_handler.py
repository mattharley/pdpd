import json
import logging

import requests
from aws_lambda_typing import context as lambda_context, events

from cache_util import ttl_cache

DEFAULT_HEADERS = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}

logger = logging.getLogger(__name__)


@ttl_cache(maxsize=128, ttl=15 * 60)
def talks_future() -> list[dict[str, str]]:
    """Get list of future talks"""
    events_list = []
    response = requests.get("https://api.meetup.com/Perth-Django-Users-Group/events/")
    if response.status_code == 200:
        data = response.json()
        sorted_data = sorted(data, key=lambda d: d["time"])
        for event in sorted_data:
            events_list.append(
                {
                    "name": event["name"],
                    "time": event["time"],
                    "venue": event.get("venue", ""),
                    "attendance": event["yes_rsvp_count"],
                    "description": event["description"],
                    "link": event["link"],
                }
            )
    return events_list


def handler(event: events.APIGatewayProxyEventV1, context: lambda_context):
    try:
        logger.info(event)
        # data: dict = json.loads(event["body"])

        response_body: list[dict] = talks_future()
        logger.info(response_body)
        return {
            "statusCode": 200,
            "headers": DEFAULT_HEADERS,
            "body": json.dumps(response_body),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": DEFAULT_HEADERS,
            "body": json.dumps({"error": e.__class__, "message": str(e)}),
        }
