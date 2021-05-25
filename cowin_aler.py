import requests
from datetime import date
import time
from audioplayer import AudioPlayer


"""
Please specify the following parameters

age ---> Mandatory
Pincode ---> Mandatory
Vaccine ----> optional either ""  or COVAXIN, COVISHIELD, SPUTNIK

"""

age=45
vaccine="COVISHELD"
pincode='600095'
today = date.today().strftime("%d-%m-%Y")
available_center=dict()

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={}&date={}".format(pincode,today)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


while not(available_center):
    result = requests.get(url, headers=headers)
    if result.status_code==200:
        for center in result.json()["centers"]:
            for slot in center['sessions']:
                if age>=slot["min_age_limit"] and slot["available_capacity_dose1"]>0 and (vaccine=="" or vaccine==slot["vaccine"] ):                    
                    available_center[center['name']]={'vaccine': slot['vaccine'],'date':slot['date']}
        if not(available_center):
            print("refrehing")
            time.sleep(30)        
                    
    else:
        print("Api error.....retrying")
        time.sleep(30)


for center in available_center:
    print('-------------------Centers------------------')
    print('Name :{}'.format(center))
    print('Vaccine :{}'.format(available_center[center]['vaccine']))
    print('Date :{}'.format(available_center[center]['date']))
    print('--------------------------------------------\n')
audio=AudioPlayer(r"./audio/alarm-buzzer-407.mp3")
audio.play(block=False)
time.sleep(30)
    

