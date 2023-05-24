# Send a message to users that have responded in a particular way to a message

import logging
import os

from swc_slack.utils import (
    get_client,
    get_reaction_users,
    get_reactions,
    join_channel,
    send_message_to_user,
)

logging.basicConfig(level=logging.INFO)

slack_token = os.environ["SLACK_BOT_TOKEN"]


channel_id = "C85MF2VTJ"  # SWC general
text = (
    "Hello, another (more organised) course update. "
    "There are now four planned courses"
)
reaction_name = "camera_with_flash"

test_user_id = "UF9ACJLNS"  # AT
message = (
    "Hello!\nThanks for signing up to the "
    "*Introduction to Image Analysis* course. "
    "It will be held in the *SWC Lecture Theatre 10am-4pm on May 30th "
    "(next Tuesday)*. \n\nThe course materials can be found "
    "<https://software-skills.neuroinformatics.dev/"
    "courses/introduction-image-analysis.html|here>. "
    "\nIf you have any questions, please contact me (<@UF9ACJLNS>). "
    "\n\nThanks, \nAdam\n\n\n"
    "P.S. This message was sent automatically. "
    "If it looks weird, please let me know!"
)
client = get_client(slack_token)
join_channel(client, channel_id)
reactions = get_reactions(client, channel_id, text, limit=200)
user_list, username_list, email_list = get_reaction_users(
    client, reactions, reaction_name
)

print(f"{len(user_list)} users responded with: {reaction_name}")
print("Sending test message to test user...")
send_message_to_user(client, test_user_id, message)
word = input("Please type 'continue' to message all users: ")
if word == "continue":
    print("Continuing...")
    for user_id in user_list:
        print(f"Messaging: {user_id}")
        # send_message_to_user(client, user_id, message)
else:
    print("Word is not correct, aborting...")
