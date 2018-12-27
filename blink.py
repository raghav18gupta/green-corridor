import RPi.GPIO as GPIO
import time
import json
import requests

pi_info = [32781349, 'GPO Square', 22.70741081237793, 75.87882995605469]
pi_id = pi_info[0]

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

def distance(point1, point2):
    # print('point1 = {}'.format(point2))
    lat1 = radians(point1[0])
    lon1 = radians(point1[1])
    lat2 = radians(point2[0])
    lon2 = radians(point2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # approximate radius of earth in km
    R = 6378.0

    distance = R * c

    return distance


def main():
    global pi_id
    while True:
        if pi_id = read_red():
            print('in if')
            requests.get('https://api.thingspeak.com/update?api_key=6V7RH56WDZ0194HN&field1=0')
            while pi_id != read_normal():
                blink_red()
        else:
            print('in else')
            while pi_id != read_red():
                blink_normal()
            requests.get('https://api.thingspeak.com/update?api_key=S75BT7WVE6N658BI&field1=0')
                    
def read_red():
    link = 'https://api.thingspeak.com/channels/472703/feeds.json?api_key=3FYWDILHIM6QPGGX&results=1'
    req = requests.get(link).text
    req = json.loads(req)
    ret = req['feeds'][0]['field1']
    print('read_red() = {}'.format(ret))
    return float(ret)
              
def read_normal():
    link = 'https://api.thingspeak.com/channels/472702/feeds.json?api_key=GHA2QQD9V4BPUB03&results=1'
    req = requests.get(link).text
    req = json.loads(req)
    ret = req['feeds'][0]['field1']
    print('read_normal() = {}'.format(ret))
    return float(ret)
    

def blink_normal():
    GPIO.output(7, True)
    GPIO.output(11, False)
    GPIO.output(13,  False)
    time.sleep(5)

    GPIO.output(7, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    time.sleep(1)

    GPIO.output(7, False)
    GPIO.output(11, False)
    GPIO.output(13, True)
    time.sleep(5)

    GPIO.output(7, False)
    GPIO.output(11, True)
    GPIO.output(13,  False)
    time.sleep(1)            

def blink_red():
    GPIO.output(7, True)
    GPIO.output(11, False)
    GPIO.output(13,  False)
    time.sleep(5)

try:
    main()
except:
    GPIO.cleanup()
