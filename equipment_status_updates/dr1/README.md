# DR1 Notification Slackbot
This script implements a Slackbot that reports the status of DR1 (Bluefors dilution refrigerator) in the SNU Quantum Device Lab.

## Setting Up
### Installation


### Setting up Slack Incoming Webhook (adapted from https://velog.io/@king/slack-incoming-webhook)
1. https://api.slack.com 접속 > Your apps > Create your first app
2. From scratch > 앱이름(소문자와 '-'로 구성) 과 슬랙 워크스페이스 선택 > Create App
3. Collaborators > 동료 또는 또는 절대삭제 안되는 공용계정 추가 <- 이래야 퇴사자 발생 시 방어됩니다.
4. Incoming Webhooks 선택 > On > Add New Webhook to Workspace > 채널 선택 > 허용
5. Incoming Webhooks 선택 > Webhook URL 값 확인

### Setting up Configuration
It is necessary to modify variables of the `config.py` file to specify an appropriate path of the log files and the URL that the message is sent to.
- `BF_LOG_FOLDER`: path to the bluefors log folder. It is recommended to use a local folder (computer connected to Bluefors Control Unit) for stability.
- `SLACK_WEBHOOK_URL`: URL that the slack webhook is sent to (see the above instrucitons for details).
- `active_temp_ch`: a dictionary containing the mapping between active temperature channels to the corresponding sensor locations.

### Testing Script
In the command prompt, execute
```bash
$python log_dr1.py
```

## Task Scheduler (Windows)