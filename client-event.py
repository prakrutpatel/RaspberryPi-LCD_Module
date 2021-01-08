import pickle
import datetime
from apiclient.discovery import build
import requests,json
import socket

ClientSocket = socket.socket()
host='127.0.0.1'
port = 1233


try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
now = datetime.datetime.utcnow().isoformat() + 'Z'

events_result = service.events().list(calendarId='primary', timeMin=now,maxResults=1, singleEvents=True,orderBy='startTime').execute()
events = events_result.get('items', [])
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    ori=start.find('T')
    dub1=start[ori+1:len(start)]
    dub2=dub1.find('-')
    new=dub1[0:dub2]
message = {
    "1": str(event['summary']),
    "2": new,
    "time": 5,
    "priority": "High"
}
data=json.dumps(message)
ClientSocket.send(bytes(data, 'utf-8'))

ClientSocket.close()
