import boto3
import os
import json
import logging

import urllib3
http = urllib3.PoolManager()

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_event(event):
    logger.info(json.dumps(event))

    if 'type' not in event:
        logger.info("Unable to parse event.")
        return None

    type = event['type']
    if type not in ['LOGIN', 'LOGIN_ERROR']:
        logger.info(f"No need to handle {type} event.")
        return None

    realmId = event['realmId']
    clientId = event['clientId']

    color = 0
    if type == "LOGIN":
        color = 2752256 # Green
    if type == "LOGIN_ERROR":
        color = 16711680 # Red

    username = event['details']['username']

    return {
      "content": None,
      "embeds": [
        {
          "description": f"{type} - **{username}**",
          "color": color,
          "fields": [
            {
                "name": "Realm",
                "value": f"`{realmId}`",
                "inline": True
            },
            {
                "name": "Client",
                "value": f"`{clientId}`",
                "inline": True
            },
          ]
        }
      ]
    }


def notify_via_discord(content):
    url = os.environ['DISCORD_URL']
    r = http.request('POST', url,
        body=json.dumps(content).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
        },
        timeout=10)
    if r.status != 204:
        logger.error(f"Unexpected response from Discord ({r.status}): {r.data}")
        return False

    logger.info(f"Message sent to Discord (status: {r.status})")
    return True


def lambda_handler(event, context):
    logger.info(json.dumps(event))

    discord_content = parse_event(json.loads(event['body']))
    logger.info(json.dumps(discord_content))
    if discord_content is not None:
        notify_via_discord(discord_content)
