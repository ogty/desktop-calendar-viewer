from datetime import datetime, timedelta
import os
import subprocess

from dotenv import load_dotenv
import googleapiclient.discovery
import google.auth


load_dotenv()


CALENDAR_ID = os.environ["CALENDAR_ID"]
PERIOD = os.environ["PERIOD"]
FILE_NAME = os.environ["FILE_NAME"]
START_FORMAT = os.environ["START_FORMAT"]
END_FORMAT = os.environ["END_FORMAT"]

BASE_DIR = os.path.dirname(__file__)
HOME_DIR = os.environ["HOME"]
DESKTOP_PATH = os.path.join(HOME_DIR, "Desktop")
FILE_PATH = os.path.join(DESKTOP_PATH, f"{FILE_NAME}.txt")


auth_url = ["https://www.googleapis.com/auth/calendar"]
gapi_creds = google.auth.load_credentials_from_file(f"{BASE_DIR}/credentials.json", auth_url)[0]
service = googleapiclient.discovery.build("calendar", "v3", credentials=gapi_creds)

utc_now_str = datetime.utcnow().isoformat()
time_min = utc_now_str + 'Z'
time_max = datetime.fromisoformat(utc_now_str) + timedelta(days=int(PERIOD))
time_max = time_max.isoformat() + 'Z'

events = service.events().list(
    calendarId=CALENDAR_ID,
    timeMin=time_min,
    timeMax=time_max,
    singleEvents=True,
    orderBy="startTime",
).execute()


string_schedules = ''
schedules = events["items"]
for schedule in schedules:
    summary = schedule["summary"]
    start = datetime.fromisoformat(schedule["start"]["dateTime"]).strftime(START_FORMAT)
    end = datetime.fromisoformat(schedule["end"]["dateTime"]).strftime(END_FORMAT)
    string_schedules += f"{start} ~ {end} | {summary}\n"

with open(f"{DESKTOP_PATH}/{FILE_NAME}.txt", 'w', encoding="utf-8") as f:
    f.write(string_schedules)

today = datetime.now().day
subprocess.run(["ic", "conv", f"{FILE_PATH}@google-calendar-{today}"])
