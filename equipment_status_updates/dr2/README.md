# DR2 Notification Slackbot
This script implements a Slackbot that reports the status of DR2 (Bluefors dilution refrigerator) in the SNU Quantum Device Lab.

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
- `scheduled_times`: a list of strings that represent scheduled reporting times everyday in the `"hh:mm"` format.

### Testing Script
In the command prompt, execute
```bash
$python <path_to_this_directory>\log_dr2.py
```
in order to test the output. You need to make sure that the bot is posting the correct message to the desired Slack channel.

## Task Scheduler (Windows)
1. Open Task Scheduler. Press Win + S → type Task Scheduler → open it
2. Click Create Task (not "Basic Task"). This gives you more control.
3. General Tab
    - Name: DR2-StatusBot Startup
    - Check: "Run whether user is logged on or not"
    - Check: "Run with highest privileges"
    - Configure for: your OS version
4. Triggers Tab
    - Click New
    - Set "Begin the task" to: At startup
    - Click OK
5. Actions Tab
    - Click New
    - Action: Start a program
    - Program/script: path to your Python interpreter, e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`
    - Add arguments (your script path in quotes), e.g., `C:\Users\YourName\SNU-QDL-Slackbots\equipment_status_updates\dr2\log_dr2.py`
    - Start in (optional): directory where the script resides, e.g., `C:\Users\YourName\SNU-QDL-Slackbots\equipment_status_updates\dr2\`
6. Click OK. It may prompt for your Windows password (because it will run in the background)

