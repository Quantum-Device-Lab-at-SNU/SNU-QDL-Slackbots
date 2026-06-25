import pint
import datetime, time, schedule
import pygetwindow as gw
import pyautogui
from slack_sdk import WebClient

from config import PLASSYS_MODEL, PLASSYS_NAME, SCREENSHOT_PATH, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, testing, scheduled_times

ureg = pint.UnitRegistry()

def datestr(yesterday = False):
    now = datetime.datetime.now()
    
    if not yesterday:
        ymd_str = (
            str(now.year)[-2:],
            str('{:02d}'.format(now.month)),
            str('{:02d}'.format(now.day))
        )
    else:
        prev_day = now - datetime.timedelta(days=1)
        ymd_str = (
            str(prev_day.year)[-2:],
            str('{:02d}'.format(prev_day.month)),
            str('{:02d}'.format(prev_day.day))
        )
    return '%s-%s-%s' % ymd_str

def status_message(): # Todo: implement status message for Plassys e-beam evaporator
    """Create a status update message to be sent to Slackbot

    Returns:
        str: status update message
    """

    return ""

def capture_program_window(title_keyword, output_path=SCREENSHOT_PATH):
    matches = [
        w for w in gw.getWindowsWithTitle(title_keyword)
        if w.title and w.width > 0 and w.height > 0
    ]

    if not matches:
        raise RuntimeError(f"No window found containing title: {title_keyword}")

    window = matches[0]

    # Bring the program to the front
    window.restore()
    time.sleep(0.5)  # Wait for the window to restore
    window.activate()

    # Capture only that window region
    screenshot = pyautogui.screenshot(region=(
        window.left,
        window.top,
        window.width,
        window.height,
    ))

    screenshot.save(output_path)
    return output_path

def post_to_slack():

    message = status_message()
    screenshot_path = capture_program_window('Top', output_path=SCREENSHOT_PATH)

    client = WebClient(token=SLACK_BOT_TOKEN)

    client.files_upload_v2(
        channel=SLACK_CHANNEL_ID,
        file=screenshot_path,
        title=f"{PLASSYS_NAME} {PLASSYS_MODEL} Control Screenshot",
        initial_comment=message,
    )



if __name__ == '__main__':
    # for testing status message
    if testing:
        msg = status_message()
        print(msg)
        post_to_slack()
    else:
        # post to slack when first executed
        post_to_slack()

        # Schedule the task at specific times
        for _t in scheduled_times:
            schedule.every().day.at(_t).do(post_to_slack)

        _error_status = False
        while True:
            if _error_status:
                pass            # TODO: section to implement Slack channel notification in case of error
            else:
                schedule.run_pending()
            time.sleep(60)    # check every 60 sec

