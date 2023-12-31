import datetime, re
import googleapiclient.discovery
import google.auth

def get_calen():
     # Preparation for Google API
     SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
     calendar_id = 'utakka15@gmail.com'
     gapi_creds = google.auth.load_credentials_from_file('reazon-396307-93d242895e5e.json', SCOPES)[0]
     service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)
     
     # Get events from Google Calendar API
     now = datetime.datetime.utcnow().isoformat() + '+09:00' 
     one_week_later = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + '+09:00'
     events_result = service.events().list(
          calendarId=calendar_id, timeMin=now, timeMax=one_week_later,
          maxResults=1000, singleEvents=True,
          orderBy='startTime').execute()
     
     # Pick up only start time, end time and summary info
     events = events_result.get('items', [])
     formatted_events = [(event['start'].get('dateTime', event['start'].get('date')), # start time or day
          event['end'].get('dateTime', event['end'].get('date')), # end time or day
          event['summary']) for event in events]
     
     # Generate output text
     response = ''
     '''
     for event in formatted_events:
          if re.match(r'^\d{4}-\d{2}-\d{2}$', event[0]):
               start_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[0], '%Y-%m-%d'))
               end_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%d'))
               response += '{0} ~ {1}、'.format(start_date, end_date)
          else:
               start_time = '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00'))
               end_time = '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S+09:00')) # この行が問題でした
               response += '{0} ~ {1}、'.format(start_time, end_time)
     
     '''
     for event in formatted_events:
          if re.match(r'^\d{4}-\d{2}-\d{2}$', event[0]):
               start_date = '{0:%Y-%m-%d}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%d'))
               response += '{0}、'.format(start_date)
          # For all day events
          else:
               start_time = '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.strptime(event[0], '%Y-%m-%dT%H:%M:%S+09:00'))
               end_time = '{0:%H:%M}'.format(datetime.datetime.strptime(event[1], '%Y-%m-%dT%H:%M:%S+09:00'))
               response += '{0} ~ {1}、'.format(start_time, end_time)
     
     response = response.rstrip(',')
     return response