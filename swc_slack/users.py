from typing import List, Tuple

from slack_sdk import WebClient


def get_users(client: WebClient) -> List[dict]:
    response = client.users_list()
    users = response["members"]
    return users


def get_user_info(client: WebClient, user_id: str) -> Tuple[str, str]:
    response = client.users_info(user=user_id)

    user_name = response["user"]["name"]
    user_email = response["user"]["profile"]["email"]
    return user_name, user_email


def get_reaction_users(
    client: WebClient, reactions: List[dict], reaction_name: str
) -> Tuple[List[str], List[str], List[str]]:
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


def get_ids_of_specific_users_by_email(
    client: WebClient, emails: List[str]
) -> List[str]:
    all_users = get_users(client)
    users = []
    for user in all_users:
        for email in emails:
            try:
                if email in user["profile"]["email"]:
                    users.append(user["id"])
            except KeyError:
                pass
    return users
