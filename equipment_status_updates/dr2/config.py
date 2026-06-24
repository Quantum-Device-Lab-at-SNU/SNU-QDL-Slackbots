# Slack bot configuration
SLACK_BOT_TOKEN = "xoxb-..."
SLACK_CHANNEL_ID = "C0XXXXXXX"
SCREENSHOT_PATH = "bluefors_screenshot.png"

# DR specific configuration
BF_LOG_FOLDER = ".../Bluefors logs"
DR_NAME = "DR"  # name of the dilution refrigerator (for logging purposes) e.g., "DR1", "DR2", etc.

# list of temperature channels to report
active_temp_ch = {
    "CH1 T": "50K Flange",
    "CH2 T": "4K Flange",
    "CH5 T": "Still Flange",
    "CH6 T": "MXC Flange"
}

# status update times (str in "hh:mm" format)
scheduled_times = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]

# variable to indicate if you are testing
testing = True