from typing import List

from slack_sdk import WebClient


def send_message_to_user(client: WebClient, user_id: str, message: str):
    response = client.conversations_open(users=user_id)
    channel = response["channel"]["id"]
    client.chat_postMessage(channel=channel, text=message)


def safe_send_message_to_users(
    client: WebClient,
    user_list: List[str],
    message: str,
    password: str = "continue",
):
    word = input(f"Please type '{password} to message all users: ")
    if word == password:
        print("Continuing...")
        for user_id in user_list:
            print(f"Messaging: {user_id}")
            send_message_to_user(client, user_id, message)
    else:
        print("Word is not correct, aborting...")
