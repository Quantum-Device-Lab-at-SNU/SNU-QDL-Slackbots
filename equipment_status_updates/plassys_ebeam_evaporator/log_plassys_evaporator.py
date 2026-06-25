import pandas as pd
import numpy as np
import pint
from pathlib import Path
import datetime, time, schedule
import pygetwindow as gw
import pyautogui
from slack_sdk import WebClient

from config import PLASSYS_MODEL, PLASSYS_NAME, PLASSYS, SCREENSHOT_PATH, SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, active_temp_ch, testing, scheduled_times

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

def status_message():
    """Create a status update message to be sent to Slackbot (incoming Webhooks)

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
    screenshot_path = capture_program_window('Bluefors Control Software Frontend', output_path=SCREENSHOT_PATH)

    client = WebClient(token=SLACK_BOT_TOKEN)

    client.files_upload_v2(
        channel=SLACK_CHANNEL_ID,
        file=screenshot_path,
        title=f"{PLASSYS_NAME} {PLASSYS_MODEL} Control Screenshot",
        initial_comment=message,
    )


#   TODO: check compressor status, turbopump, etc., to make a notification in case of abnormal signs.
#  activated_cpa_ch = {
#     'cpatempwi': 'Input water temp.',
#     'cpatempwo': 'Output water temp.',
#     'cpatempo': 'Oil temp.',
#     'cpatemph': 'Helium temp.',
#     'cpalp': 'Low side pressure',
#     'cpahp': 'Low side pressure',
#     'cpalpa': 'Avg. low side pressure',
#     'cpahpa': 'Avg. high side pressure',
#     'cpadp': 'Delta pressure',
#     'cpacurrent': 'Current',
#     'cpahours': 'Running hours'
# }

# activated_turbo_ch = {
#     'tc400actualspd': 'Rot. Freq.',
#     'tc400drvpower': 'Drive Power',
#     'tc400ovtemppum': 'Pump temp. too high'
# }

# def latest_cpa_status():
    
#     ''
#     {'Status'}
# 06-05-25,23:30:01,ctrl_pres_ok,1.000000e+00,ctrl_pres,1.000000e+00,
# cpastate,3.000000e+00,cparun,1.000000e+00,cpawarn,-0.000000e+00,cpaerr,-0.000000e+00,cpatempwi,2.023500e+01,cpatempwo,3.225611e+01,cpatempo,3.615778e+01,cpatemph,7.086166e+01,cpalp,8.335809e+01,cpalpa,8.036925e+01,cpahp,2.869694e+02,cpahpa,2.842413e+02,cpadp,2.033709e+02,cpacurrent,1.518404e+01,cpahours,2.012210e+04,cpascale,0.000000e+00,cpasn,1.092400e+04,ctr_pressure_ok,1.000000e+00,
# tc400actualspd,0.000000e+00,tc400drvpower,0.000000e+00,tc400ovtempelec,0.000000e+00,tc400ovtemppum,0.000000e+00,tc400heating,0.000000e+00,tc400pumpaccel,0.000000e+00,tc400pumpstatn,1.000000e+00,tc400remoteprio,1.000000e+00,tc400spdswptatt,0.000000e+00,tc400setspdatt,0.000000e+00,tc400standby,0.000000e+00,
# tc400actualspd_2,0.000000e+00,tc400drvpower_2,1.000000e+00,tc400ovtempelec_2,0.000000e+00,tc400ovtemppum_2,0.000000e+00,tc400heating_2,0.000000e+00,tc400pumpaccel_2,0.000000e+00,tc400pumpstatn_2,1.000000e+00,tc400remoteprio_2,1.000000e+00,tc400spdswptatt_2,0.000000e+00,tc400setspdatt_2,0.000000e+00,tc400standby_2,0.000000e+00
# #Pulse Tube, HS-STILL, HS-MC, EXT, 4K HEATER
# def pump_status():
#     # note: this only reports the pump status in the software only; may not reflect the actual status of the pump hardware

# # pump status



# status = read_latest_status("path/to/status.csv")
# message = f"""🧊 Bluefors Status Update:
# Time: {status['Time']}
# MC Temp: {status['MC Temp']} mK
# Still Temp: {status['Still Temp']} K
# Pressure: {status['Pressure']} mbar
# """
# post_to_slack(message, SLACK_WEBHOOK_URL)


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

