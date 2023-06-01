from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_client(slack_token: str) -> WebClient:
    return WebClient(token=slack_token)


def join_channel(client: WebClient, channel_id: str) -> None:
    try:
        response = client.conversations_join(channel=channel_id)
        if response["ok"]:
            print("Successfully joined the channel.")
        else:
            print(f"Error: {response['error']}")
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")


def convert_email_list_to_copyable_string(email_list: str) -> str:
    emails_string = "; ".join(email_list)
    return emails_string
