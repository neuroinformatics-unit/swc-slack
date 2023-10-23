# swc-slack

Tools to streamline the use of Slack at SWC, e.g. for automating messages to course attendees.

## Installation

Download and install the package using pip
```bash
git clone https://github.com/neuroinformatics-unit/swc-slack
cd swc-slack
pip install .
```

Set up authentication:

* Firstly, go to the [Neuroinformatics Unit Slack app page](https://api.slack.com/apps/A0595H3B6H3)
(if you don't have access, contact Adam)
* Navigate to "OAuth & Permissions"
* Copy the "Bot User OAuth Token"
* Set this as an environmental variable on your machine. e.g.
  `SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXXXXXXXXX`

## Usage
Set slack token from environmental variable
```python
slack_token = os.environ["SLACK_BOT_TOKEN"]
```

Initialise Slack client
```python
from swc_slack.utils import get_client
client = get_client(slack_token)
```

Search for all users that responded to a specific message with a specific reaction
```python
channel_id = "D55JK0ABC"  # Copy a message link to find this
reaction_name = "penguin" # Can be anything

from swc_slack.messaging.read import get_message_emoji_respondents

user_list, _, _ = get_message_emoji_respondents(
    client, channel_id, text, reaction_name
)
```

Message a specific user

```python
from swc_slack.messaging.write import send_message_to_user

send_message_to_user(client, UA8ABCXYZ, "Hello there!")
```

Message many users (with a confirmation step to prevent accidental spam)

```python
from swc_slack.messaging.write import safe_send_message_to_users
safe_send_message_to_users(client, user_list, "Hello everyone!")
# Type "continue" at the prompt to send the message
```

## Examples:
* [Messaging all users who responded to a message with a specific reaction](https://github.com/neuroinformatics-unit/swc-slack/blob/main/scripts/message_image_analysis_attendees.py) (e.g. as an easy way to sign up to a course).

## Notes
* To find the ID of a specific channel, copy the link to a message in the
channel, and the ID will be the penultimate part of the URL. e.g.
`https://workspace.slack.com/archives/CHANNEL_ID/xyz`
* To find the ID of an individual, click on their profile within Slack,
  then click the three dots, and select "Copy member ID".
* Beware that Slack allows users to specify a skin tone for emojis.
  Therefore, an emoji with a specific skin tone will be different from the
  default. If relying on this, it may be easier to choose inanimate emojis.

## Limitations
* I'm not currently aware of any unique message ID, so this must be
  searched for using text contained in the message
