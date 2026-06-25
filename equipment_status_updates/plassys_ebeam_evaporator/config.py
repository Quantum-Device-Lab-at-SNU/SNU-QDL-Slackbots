# Slack bot configuration
SLACK_BOT_TOKEN = "xoxb-..."
SLACK_CHANNEL_ID = "C0XXXXXXX"
SCREENSHOT_PATH = "bluefors_screenshot.png"

# Plassys specific configuration
PLASSYS_LOG_FOLDER = ".../Bluefors logs"
PLASSYS_NAME = "Plassys"   # name of the e-beam evaporator (for logging purposes) e.g., "Plassys", etc.
PLASSYS_MODEL = "MEB550S"  # model of the e-beam evaporator (for logging purposes) e.g., "MEB550S", etc.

# # list of temperature channels to report
# active_temp_ch = {
#     "CH1 T": "50K Flange",
#     "CH2 T": "4K Flange",
#     "CH5 T": "Still Flange",
#     "CH6 T": "MXC Flange"
# }

# status update times (str in "hh:mm" format)
scheduled_times = ["01:00", "04:00", "07:00", "10:00", "13:00", "16:00", "19:00", "22:00"]

# variable to indicate if you are testing
testing = True