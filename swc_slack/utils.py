from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_client(slack_token):
    return WebClient(token=slack_token)


def get_users(client):
    try:
        response = client.users_list()
        if response["ok"]:
            users = response["members"]
            for user in users:
                print(user["name"])
        else:
            print(f"Error: {response['error']}")
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")


def join_channel(client, channel_id):
    try:
        response = client.conversations_join(channel=channel_id)
        if response["ok"]:
            print("Successfully joined the channel.")
        else:
            print(f"Error: {response['error']}")
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")


def get_reactions(client, channel_id, text, limit=100):
    response = client.conversations_history(channel=channel_id, limit=limit)

    for message in response["messages"]:
        if "text" in message and text in message["text"]:
            reactions = message["reactions"]
            return reactions
            break
    else:
        print("Message not found.")


def get_user_info(client, user_id):
    response = client.users_info(user=user_id)

    user_name = response["user"]["name"]
    user_email = response["user"]["profile"]["email"]
    return user_name, user_email


def get_reaction_users(client, reactions, reaction_name):
    user_list = []
    username_list = []
    email_list = []
    for reaction in reactions:
        if reaction["name"] == reaction_name:
            users = reaction["users"]
            for user in users:
                user_list.append(user)
                user_name, user_email = get_user_info(client, user)
                username_list.append(user_name)
                email_list.append(user_email)
    return user_list, username_list, email_list


def convert_email_list_to_copyable_string(email_list):
    emails_string = "; ".join(email_list)
    return emails_string


def send_message_to_user(client, user_id, message):
    response = client.conversations_open(users=user_id)
    channel = response["channel"]["id"]
    client.chat_postMessage(channel=channel, text=message)
