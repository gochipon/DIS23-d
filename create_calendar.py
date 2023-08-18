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

print('予定名:')
name = input()
print('年:',end = '')
year = int(input())
print('月:',end = '')
month = int(input())
print('日:',end = '')
day = int(input())
print('開始時間を　00:00 形式:',end = '')
first_time = list(input().split(':'))
print('修了時間を　00:00 形式:',end = '')
last_time = list(input().split(':'))

# ②予定を書き込む
# 書き込む予定情報を用意する
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