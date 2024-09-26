"""
Send message to all users that have responded to a particular message
with one of many available reactions.
"""

import logging
import os

from swc_slack.messaging.read import get_message_emoji_respondents
from swc_slack.messaging.write import (
    safe_send_message_to_users,
    send_message_to_user,
)
from swc_slack.utils import get_client

logging.basicConfig(level=logging.INFO)

slack_token = os.environ["SLACK_BOT_TOKEN"]

# Channel ID and message text to search for
channel_id = "C85MF2VTJ"  # SWC general
text = (
    'will be giving a series of "Software skills for systems neuroscience" '
    'courses between September 30th and October 8th.'
)

# Reaction names to search for
reaction_names = [
    "snake",  # Introduction to Python
    "floppy_disk",  # Data Management
    "mortar_board",  # Git and best practices
    "video_camera",  # Behavioural analysis
    "desktop_computer",  # Linux and HPC
    "microscope",  # General Microscopy
    "microbe",  # Histology analysis
]

# Message to send to users
message = (
    "Hello!\n\nYou are receiving this message because you have signed up to "
    "one or more of our software skills courses, which will run between 30 "
    "September and 8th October. You can find the detailed schedule on the "
    "<https://software-skills.neuroinformatics.dev/courses/software-skills.html|course website>."
    "\n\nPlease follow "
    "<https://neuroinformatics.dev/slides-SWC-PhD-intro/#/section|these installation instructions> "
    "in advance (you can skip them if you are confident you have alternatives "
    "installed and know how to use them). If you have any questions, "
    "please contact Adam (<@UF9ACJLNS>).\n\nThanks, \nThe NIU team\n\n\n "
    "P.S. This message was sent automatically. "
    "If it looks weird, please let us know!"
)

# Get Slack client
client = get_client(slack_token)

user_set = set()
for reaction_name in reaction_names:
    # Get list of user IDs that responded with each reaction
    user_list, username_list, email_list = get_message_emoji_respondents(
        client, channel_id, text, reaction_name
    )
    print(f"{len(user_list)} users responded with {reaction_name}.")
    user_set.update(user_list)

print(f"Total unique users that reacted: {len(user_set)}")

# Add extra users that did not respond with reactions,
# but instead sent us a message
extra_users = ["U0241NLGA75", "U06A40MJVK5"]
user_set.update(extra_users)
print(f"Added {len(extra_users)} extra users to the list.")
print(f"Total users to be messaged: {len(user_set)}")

# Send message to test user
print("Sending test message to test user...")
test_user_id = "U044NSQ8PT8"  # NS
send_message_to_user(client, test_user_id, message)

# Send message to all users that responded with any of the reactions
safe_send_message_to_users(client, list(user_set), message)
