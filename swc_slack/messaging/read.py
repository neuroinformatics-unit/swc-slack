from typing import List, Tuple

from slack_sdk import WebClient

from swc_slack.users import get_reaction_users
from swc_slack.utils import join_channel


def get_reactions(
    client: WebClient, channel_id: str, text: str, limit: int = 100
) -> List[dict]:
    response = client.conversations_history(channel=channel_id, limit=limit)

    for message in response["messages"]:
        if "text" in message and text in message["text"]:
            reactions = message["reactions"]
            return reactions
    else:
        raise ValueError("Message not found.")


def get_message_emoji_respondents(
    client: WebClient, channel_id: str, text: str, reaction_name: str
) -> Tuple[List[str], List[str], List[str]]:
    """
    Send a message to users that have responded in a particular
    way to a message
    :param client: slack_sdk.WebClient
    :param channel_id: ID of the channel in which the message
    was sent (e.g. "C21MF2VTK")
    :param text: text to search for in the channel. I.e. the message
    sent (and only this message) should contain this
    text.
    :param reaction_name: Name of the reaction (emoji) to search for.
    e.g. "camera_with_flash"
    :return: user_list, username_list, email_list
    """

    join_channel(client, channel_id)
    reactions = get_reactions(client, channel_id, text, limit=200)
    user_list, username_list, email_list = get_reaction_users(
        client, reactions, reaction_name
    )
    return user_list, username_list, email_list
