# provide a path to Bluefors log folder
BF_LOG_FOLDER = ".../Bluefors logs"

# slack webhook url
SLACK_WEBHOOK_URL = r"https://hooks.slack.com/services/..."

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