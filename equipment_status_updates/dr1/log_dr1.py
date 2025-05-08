import pandas as pd
import numpy as np
import pint
import datetime, requests, time, schedule
from config import BF_LOG_FOLDER, SLACK_WEBHOOK_URL, activated_temp_ch, testing, scheduled_times


now = datetime.datetime.now()
datestr = '%s-%s-%s' % (str(now.year)[-2:], str('{:02d}'.format(now.month)), str('{:02d}'.format(now.day)))

ureg = pint.UnitRegistry()

def latest_pressure_status():
    """Get latest pressure status from Bluefors log files

    Returns:
        dict: a dictionary consisting of quantity names and logged values
    """
    filePath = '%s/%s/maxigauge %s.log' % (BF_LOG_FOLDER, datestr, datestr)

    df = pd.read_csv(filePath)
    latest = df.iloc[-1]

    # get timestamp
    timestamp = [int(x) for x in latest.iloc[0].split('-')][::-1]  # DD-MM-YY format parsed and reversed in order
    timestamp.extend([int(x) for x in latest[1].split(':')])  # HH:MM:SS format parsed
    timestamp[0] += 2000 # YY to YYYY format
    return {
        "timestamp": datetime.datetime(*timestamp),
        "P1": (float(latest.iloc[5]) * ureg.mbar).to_compact(),
        "P2": (float(latest.iloc[11]) * ureg.mbar).to_compact(),
        "P3": (float(latest.iloc[17]) * ureg.mbar).to_compact(),
        "P4": (float(latest.iloc[23]) * ureg.mbar).to_compact(),
        "P5": (float(latest.iloc[29]) * ureg.mbar).to_compact(),
        "P6": (float(latest.iloc[35]) * ureg.mbar).to_compact(),
    }

def latest_temp_status():
    """Get latest temperature status from Bluefors log files

    Returns:
        dict: a dictionary consisting of quantity names and logged values
    """
    temp_status = {}
    for ch in activated_temp_ch.keys():
        filePath = '%s/%s/%s %s.log' % (BF_LOG_FOLDER, datestr, ch, datestr)
        df = pd.read_csv(filePath)
        temp_status[activated_temp_ch[ch]] = (float(df.iloc[-1, 2]) * ureg.kelvin).to_compact()
    return temp_status

def latest_flow_status():
    """Get latest flow status from Bluefors log files

    Returns:
        dict: a dictionary consisting of quantity names and logged values
    """
    filePath = '%s/%s/Flowmeter %s.log' % (BF_LOG_FOLDER, datestr, datestr)
    df = pd.read_csv(filePath)
    return {'Flow': (float(df.iloc[-1, 2]) * ureg.millimol / ureg.s).to_compact()}

def lastest_channel_status():
    """Get latest channel status (as seen from Control Unit) from Bluefors log files

    Returns:
        dict: a dictionary consisting of quantity names and logged values
    """
    filePath = '%s/%s/Channels %s.log' % (BF_LOG_FOLDER, datestr, datestr)
    df = pd.read_csv(filePath)

    ch_name = np.array(df.iloc[-1, 3::2], dtype=str)
    ch_val = np.array(df.iloc[-1, 4::2], dtype=bool)

    on_channels = ch_name[ch_val]
    return {'ON Channels': on_channels}

def status_message():
    """Create a status update message to be sent to Slackbot (incoming Webhooks)

    Returns:
        str: status update message
    """
    # collect all status loading results
    pressure_status = latest_pressure_status()
    temp_status = latest_temp_status()
    flow_status = latest_flow_status()
    ch_status = lastest_channel_status()
    _status = {
        **pressure_status, **temp_status, **flow_status, **ch_status
    }

    # Green light if MXC Flange temperature is below 100mK
    mc_alarm_emoji = "🟢" if _status['MXC Flange'] < (100 * ureg.mK)  else "🔴"

    message = f"*🧊 DR1 Status Update (Time: {_status['timestamp']}, MXC Status: {mc_alarm_emoji})*\n"
    # log pressures
    message += "• _*Pressures*_ - "
    for _p_i, _p in enumerate(['P1', 'P2', 'P3', 'P4', 'P5', 'P6']):
        if _p_i != 0:
            message += ", "
        message += f"*{_p}:* {_status[_p]:.2f~P}"

    message += "\n"

    # log temperatures
    message += "• _*Temperatures*_ - "
    for _T_i, _T in enumerate(['50K Flange', '4K Flange', 'Still Flange', 'MXC Flange']):
        if _T_i != 0:
            message += ", "
        message += f"*{_T}:* {_status[_T]:.2f~P}"
    
    message += "\n"

    # log flow rate
    message += f"• _*Flow rate*_ - {_status['Flow']:.2f~P}\n"

    # log "on" channels
    message += "• _*Valves/Pumps/PT/Heat-Switches Turned ON*_ - " + ', '.join(_status["ON Channels"])

    return message

def post_to_slack():
    payload = {"text": status_message(), "link_names": 1, "mrkdwn": True}
    requests.post(SLACK_WEBHOOK_URL, json=payload)


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
        post_to_slack(msg, SLACK_WEBHOOK_URL)
    else:

        # Schedule the task at specific times
        for _t in scheduled_times:
            schedule.every().day.at(_t).do(post_to_slack)

        _error_status = False
        while True:
            schedule.run_pending()
            time.sleep(60)

