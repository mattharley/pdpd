import json
import logging
import re

import markdown
import requests
from aws_lambda_typing import context as lambda_context
from aws_lambda_typing import events
from cache_util import ttl_cache

DEFAULT_HEADERS = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}

logger = logging.getLogger(__name__)


P_PATTERN: re.Pattern = re.compile(r"<p>(.+?)</p>")
URL_PATTERN: re.Pattern = re.compile(
    r"(<a href=\""
    r"((http|https)://)?[a-zA-Z0-9./?:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9.&/?:@\-_=#])+"
    r"]\("
    r"((http|https)://)?[a-zA-Z0-9./?:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9.&/?:@\-_=#])+"
    r"\" class=\"linkified\">)"
)
END_URL_PATTERN: re.Pattern = re.compile(r"</a>\)")


def convert_markdown(md_text: str) -> str:
    """convert markdown to html"""
    p_groups = P_PATTERN.findall(md_text)
    html: str = ""
    for md_para in p_groups:
        fixed_md = URL_PATTERN.sub("", md_para)
        fixed_md = END_URL_PATTERN.sub(")", fixed_md)
        html += markdown.markdown(fixed_md, extensions=["attr_list"]) + "\n"
    return html


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
                    "description": convert_markdown(event["description"]),
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


if __name__ == "__main__":
    resp = talks_future()
    for x in resp:
        print(json.dumps(x, indent=2))
