# Bluefors DR Notification Slackbot

Automated Slackbot for reporting the status of a Bluefors dilution refrigerator in the SNU Quantum Device Lab.

The bot periodically:

1. Reads the latest Bluefors log files.
2. Collects pressure, temperature, flow rate, and active channel information.
3. Generates a formatted status report.
4. Captures a screenshot of the Bluefors Control Software window.
5. Uploads the screenshot and status report to a Slack channel.

---

## Features

- Scheduled status updates
- Pressure monitoring (P1–P6)
- Temperature monitoring
- Flow-rate monitoring
- Active valve/pump/channel reporting
- Bluefors Control Software screenshot capture
- Slack integration using a Slack App and Bot Token

---

## Requirements

- Python ≥ 3.10
- Windows operating system
- Bluefors Control Software running
- Access to the Bluefors log directory

Required Python packages:

```bash
pip install -r requirements.txt
```

---

## Installation

```bash
cd ~
git clone https://github.com/Quantum-Device-Lab-at-SNU/SNU-QDL-Slackbots.git
cd SNU-QDL-Slackbots/equipment_status_updates/bluefors_dr
```

## Slack App Setup

Required Bot Token Scopes:

- `chat:write`
- `files:write`

Install the app to the workspace and copy:

```text
xoxb-...
```

Invite the bot to the target channel and configure the channel ID.

## Configuration

Edit `config.py`:

```python
SLACK_BOT_TOKEN = "xoxb-..."
SLACK_CHANNEL_ID = "C0123456789"
SCREENSHOT_PATH = "bluefors_screenshot.png"

BF_LOG_FOLDER = r"C:\Bluefors\LogFiles"
DR_NAME = "DR1"
DR_MODEL = "LD400"
```

Configure reporting times and temperature channels as needed.

## Screenshot Capture

The bot captures the Bluefors Control Software window whose title contains:

```text
Bluefors Control Software Frontend
```

For reliable screenshot capture:

- The software must be running.
- The desktop session must be active.
- Running while Windows is locked may prevent screenshots from being captured.

## Running

Testing:

```bash
python log_bluefors_dr.py
```

Set:

```python
testing = True
```

to immediately post a status update.

For scheduled operation:

```python
testing = False
```

The script will remain running and post updates at the configured times.

## Windows Task Scheduler

Use **Run only when user is logged on** if screenshot capture is required.

## Output

The bot uploads:

- Refrigerator status summary
- Screenshot of the Bluefors Control Software

to the configured Slack channel.
