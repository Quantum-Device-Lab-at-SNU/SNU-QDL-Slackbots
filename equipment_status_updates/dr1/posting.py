import requests

def post_to_slack(message, webhook_url):
    payload = {"text": message, "link_names": 1, "mrkdwn": True}
    requests.post(webhook_url, json=payload)