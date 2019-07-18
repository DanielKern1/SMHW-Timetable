import requests, datetime, json
from time import sleep

#Get current date
date = datetime.datetime.now()
today = date.strftime("%Y-%m-%d")
#Add datetime object as well
today2 = datetime.datetime.strptime(today, "%Y-%m-%d")
notable = {'error': 'A serious server error has occurred.  Reference: a9aae7a4-ce71-402e-951e-a7c8c302a782com.teamsatchel.callisto.support.web.rest.exception.ServerErrorException: 500 null'}
global status, timetable, data

def GetAuth(user, password, school_id):
    global status, token
    status = 0
    #Set payload and data for oauth2 request
    payload = {"client_id": "55283c8c45d97ffd88eb9f87e13f390675c75d22b4f2085f43b0d7355c1f","client_secret": "c8f7d8fcd0746adc50278bc89ed6f004402acbbf4335d3cb12d6ac6497d3"}
                   
    data = {"username": user, "password": password, "school_id": school_id, "grant_type": "password",
                    "grant_type": "password", "school_id": school_id}
    temp = requests.post("https://api.showmyhomework.co.uk/oauth/token", params=payload, data=data,
                                 headers={"Accept": "application/smhw.v3+json"})
    #Parse reply data from oauth2 request
    reply = temp.text
    reply = reply.replace("'", '"')
    reply = json.loads(reply)
    token = reply["smhw_token"]
    token_expires = reply["expires_in"]
    refresh_token = reply["refresh_token"]
    
def Download():
    global status, timetable
    status = 1
    #Set headers for timetable request
    headers = {"Accept": "application/smhw.v3+json", "Authorization": "Bearer " + token}

    response = requests.get("https://api.showmyhomework.co.uk/timetable/school/20547/student/7129897?requestDate="+today,
                            headers = headers)
    #Parse data from timetable request
    json.loads(response.text)
    timetable = json.loads(response.text)

def Parse():
    global status, timetable, week, today, today_1
    status = 2
    week = timetable["weeks"][0]["days"]
    for day in week:
        if day["date"] == today:
            today_l = day["lessons"]
            for lesson in today_l:
                if lesson["classGroup"]["subject"] != "Form perio":
                    subject = lesson["classGroup"]["subject"]
                    room = lesson["room"]
                    teacher = lesson["teacher"]["title"] + " " + lesson["teacher"]["surname"] + ", " + lesson["teacher"]["forename"]
                    if room == None: room = "P.E."
                    print("Lesson: "+subject+" Room: "+room+" Teacher: " + teacher)
                    print("DONE! ----------------------------------------------------")
def Save():
    global status, timetable
    status = 3
    #Saves Timetable for quick startup
    with open("data.json", "w") as data:
        json.dump(timetable, data)

def WeekCheck():
    global status, timetable
    status = 4
    data = saved_data
    requestDate = datetime.datetime.strptime(data['requestDate'], "%Y-%m-%d")
    if requestDate <= today2 <= requestDate+datetime.timedelta(days=4):
        timetable = data

def ErrorCheck():
    global status, timetable
    status = -1

def Exit():
    global status
    status = 5
    #Raise System Exit Call after 60 seconds
    print("Wait 60 Seconds To Exit")
    sleep(60)
    raise SystemExit

#Open saved timetable
try:
    with open("data.json", "r") as data:
        saved_data = json.load(data)
except FileNotFoundError:
    GetAuth("USERNAME", "PASSWORD", "school_id")
    Download()
    ErrorCheck()
    Parse()
    Save()
    Exit()
else:
    WeekCheck()
    Parse()
    Exit()
    
    
    
    
