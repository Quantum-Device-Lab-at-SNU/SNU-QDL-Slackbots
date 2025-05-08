# DR1 Notification Slackbot
This script implements a Slackbot that reports the status of DR1 (Bluefors dilution refrigerator) in the SNU Quantum Device Lab.

## Setting Up
### Installation
1. You need a python version >= 3.10 to execute this script without problem. Additionally you need to install `pandas`, `pint`, `requests` packages in your python enviromnent.
2. Download the repository to the home directory. If you have git installed, you can do this by
```bash
$cd ~
$git clone https://github.com/Quantum-Device-Lab-at-SNU/SNU-QDL-Slackbots
```

### Setting up Slack Incoming Webhook (adapted from https://velog.io/@king/slack-incoming-webhook)
1. Go to https://api.slack.com > Your Apps > Create your first app
2. Choose "From scratch" > Enter the app name and select your Slack workspace > Click "Create App"
3. Go to "Collaborators" > Add a colleague or a shared account that should never be deleted ← This is necessary to protect against issues when someone leaves the organization.
4. Select "Incoming Webhooks" > Turn it On > Click "Add New Webhook to Workspace" > Choose a channel > Click "Allow"
5. Go back to "Incoming Webhooks" > Check and copy the Webhook URL

### Setting up Configuration
It is necessary to modify variables of the `config.py` file to specify an appropriate path of the log files and the URL that the message is sent to.
- `BF_LOG_FOLDER`: path to the bluefors log folder. It is recommended to use a local folder (computer connected to Bluefors Control Unit) for stability.
- `SLACK_WEBHOOK_URL`: URL that the slack webhook is sent to (see the above instrucitons for details).
- `active_temp_ch`: a dictionary containing the mapping between active temperature channels to the corresponding sensor locations.

### Testing Script
In the command prompt, execute
```bash
$python <path_to_this_directory>\log_dr1.py
```
in order to test the output. You need to make sure that the bot is posting the correct message to the desired Slack channel.

## Task Scheduler (Windows)
