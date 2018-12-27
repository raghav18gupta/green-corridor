from math import sin, cos, sqrt, atan2, radians
import requests
import json
import MySQLdb

# Setup MySQL connection
conn = MySQLdb.connect('localhost', 'root', 'root', 'gc')
# conn = MySQLdb.connect('greencorridor.mysql.pythonanywhere-services.com', 'greencorridor', 'root@123', 'greencorridor$default')
c = conn.cursor()

def locate_ambulance():
    # Getting the latitude and longitude of ambulance
    link_amb = 'https://api.thingspeak.com/channels/469638/feeds.json?api_key=AJQ0RSCX1UI9RUR4&results=1&location=true'
    amb = requests.get(link_amb).text
    amb = json.loads(amb)

    lati_amb = float(amb['feeds'][0]['latitude'])
    longi_amb = float(amb['feeds'][0]['longitude'])

    return [lati_amb, longi_amb]


def distance(point1, point2):
    
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


while True:

    # Reset thingspeak fields
    requests.get('https://api.thingspeak.com/update?api_key=6V7RH56WDZ0194HN&field1=0')
    requests.get('https://api.thingspeak.com/update?api_key=S75BT7WVE6N658BI&field1=0')

    # list of installed pi from MySQL database
    pi_list = []
    c.execute('SELECT * FROM pi_info')
    rows = c.fetchall()
    for eachrow in rows:
        pi_list.append(list(eachrow))
    print('\nlist of installed pi from MySQL database: ', pi_list)



    # Getting the latitude and longitude of reqested person.
    link_req = 'https://api.thingspeak.com/channels/469639/feeds.json?api_key=PJDKMW3J8LYITRS9&results=1&location=true'
    req = requests.get(link_req).text
    req = json.loads(req)

    lati_req = req['feeds'][0]['latitude']
    longi_req = req['feeds'][0]['longitude']
    print('\nGetting the latitude and longitude of reqested person.', lati_req, longi_req)



    # Getting location of ambulance
    lati_amb, longi_amb = locate_ambulance()



    if lati_req is not None and longi_req is not None:

        # get list of all squares from palasia(location of ambulance) to reqested location
        # g_api = 'https://maps.googleapis.com/maps/api/directions/json?origin=22.723840713500977, 75.88673400878906&destination={},{}&key=AIzaSyDEt3LbCWAY1GjNBTyJFPns650guvDA3ho'.format(lati_req, longi_req)
        # print(g_api)
        # data = requests.get(g_api).text
        # data = json.loads(data)
        # path_list = []

        # for i in data['routes'][0]['legs'][0]['steps']:
        #     lattitude = i['start_location']['lat']
        #     longitude = i['start_location']['lng']
        #     path_list.append([lattitude, longitude])
        # print('\nget list of all squares from palasia(location of ambulance) to reqested location: ', path_list)
        


        # Genrating list of pi to be activated as red.
        pi_activate = [[23152670, 'Palasia Square', 22.723840713500977, 75.88673400878906],
        [28571426, 'Geeta Bhavan Square', 22.717838287353516, 75.88428497314453], 
        [32781349, 'GPO Square', 22.70741081237793, 75.87882995605469], 
        [62973742, 'Indira Gandhi Square', 22.704303741455078, 75.8764877319336]]
        # for i in range(len(pi_list)):
        #     for j in range(len(path_list)):
        #         dist = distance([pi_list[i][2], pi_list[i][3]], path_list[j])

        #         if dist < 0.075:
        #             pi_activate.append(pi_list[i])
        #             break
        print('\npi to be activated are: ', pi_activate)
 

        print('-'*100)
        print('Green Corridor Started')
        for i in range(0, len(pi_activate)):
            # Make red i'th PI
            link_red = 'https://api.thingspeak.com/update?api_key=6V7RH56WDZ0194HN&field1={}'.format(pi_activate[i][0])
            requests.get(link_red)
            
            print('\nreach : {}'.format(pi_activate[i][1]))

            # Wait till ambulance reach to signal.
            while distance([pi_activate[i][2], pi_activate[i][3]], locate_ambulance()) >0.1:
                pass

            # Make again normal the i'th PI
            link_normal = 'https://api.thingspeak.com/update?api_key=S75BT7WVE6N658BI&field1={}'.format(pi_activate[i][0])
            requests.get(link_normal)

            print('reached : {}'.format(pi_activate[i][1]))

        print('Green Corridor End. Thank You')
        quit()  
