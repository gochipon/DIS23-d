import datetime
import googleapiclient.discovery
import google.auth


# ①Google APIの準備をする

SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = 'utakka15@gmail.com'
# Googleの認証情報をファイルから読み込む
gapi_creds = google.auth.load_credentials_from_file('reazon-396307-93d242895e5e.json', SCOPES)[0]
# APIと対話するためのResourceオブジェクトを構築する
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

schedule = {
  "2023-08-18": [
    {
      "start_time": "09:00",
      "end_time": "11:00",
      "task": "リーディングの問題集を解く"
    },
    {
      "start_time": "13:00",
      "end_time": "15:00",
      "task": "リスニングの問題集を解く"
    },
    {
      "start_time": "16:00",
      "end_time": "18:00",
      "task": "リーディングの模擬試験を受ける"
    },
    {
      "start_time": "19:00",
      "end_time": "21:00",
      "task": "文法の勉強"
    }
  ],
  "2023-08-19": [
    {
      "start_time": "09:00",
      "end_time": "11:00",
      "task": "リスニングの問題集を解く"
    },
    {
      "start_time": "13:00",
      "end_time": "15:00",
      "task": "リーディングの問題集を解く"
    },
    {
      "start_time": "16:00",
      "end_time": "18:00",
      "task": "リスニングの模擬試験を受ける"
    },
    {
      "start_time": "19:00",
      "end_time": "21:00",
      "task": "文法の勉強"
    }
  ]
}

events = []

for date, tasks in schedule.items():
    for task in tasks:
        start_time = task["start_time"]
        end_time = task["end_time"]
        task_description = task["task"]
        events.append([date, start_time, end_time, task_description])
        
#print(events)
# ②予定を書き込む
# 書き込む予定情報を用意する
for date, first, last, name in events:
    year, month, day = map(int, date.split('-'))
    first_time = list(map(int, first.split(':')))
    last_time = list(map(int, first.split(':')))
    body = {
        # 予定のタイトル
        'summary': name,
        # 予定の開始時刻
        'start': {
            'dateTime': datetime.datetime(year, month, day, int(first_time[0]), int(first_time[1])).isoformat(),
            'timeZone': 'Japan'
        },
        # 予定の終了時刻
        'end': {
            'dateTime': datetime.datetime(year, month, day, int(last_time[0]), int(last_time[1])).isoformat(),
            'timeZone': 'Japan'
        },
    }
    # 用意した予定を登録する
    event = service.events().insert(calendarId=calendar_id, body=body).execute()