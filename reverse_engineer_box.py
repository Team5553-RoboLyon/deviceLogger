#!/usr/bin/env python
# coding: utf-8

import requests
import json
from datetime import datetime
import pytz
from prettytable import PrettyTable

prefix = "3e673c0f"

cookies = {
    prefix + '/accept-language': 'fr,fr-FR',
    'UILang': 'fr',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': '*/*',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Authorization': 'X-Sah-Login',
    'Content-Type': 'application/x-sah-ws-4-call+json',
    'Origin': 'https://192.168.1.1',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://192.168.1.1/homeAuthentificationRemote.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
data = '{"service":"sah.Device.Information","method":"createContext","parameters":{"applicationName":"webui","username":"adminremote","password":"r5HWGRro"}}'
loginResponse = requests.post('https://192.168.1.1/ws', headers=headers, cookies=cookies, data=data, verify = False)


# loginResponse.cookies.get_dict()['45b4c072/sessid']
# json.loads(loginResponse.text)['data']['contextID']

cookies = {
    prefix + '/accept-language': 'fr,fr-FR',
    'UILang': 'fr',
    prefix + '/sessid': loginResponse.cookies.get_dict()[prefix + '/sessid'],
    'sah/contextId': json.loads(loginResponse.text)['data']['contextID'],
}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': '*/*',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'X-Sah-Request-Type': 'idle',
    'Content-Type': 'application/x-sah-ws-4-call+json',
    'Authorization': 'X-Sah ' +json.loads(loginResponse.text)['data']['contextID'],
    'X-Context': json.loads(loginResponse.text)['data']['contextID'],
    'Origin': 'https://192.168.1.1',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://192.168.1.1/homeAuthentificationRemote.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
data = '{"service":"TopologyDiagnostics","method":"buildTopology","parameters":{"SendXmlFile":false}}'
dataResponse = requests.post('https://192.168.1.1/ws', headers=headers, cookies=cookies, data=data, verify=False)


t = PrettyTable(['A', 'B', 'C', "D"])

for i in json.loads(dataResponse.text)['status'][0]['Children'][0]['Children']:
    if 'Children' in i:
        for j in i['Children']:
            if j['Active']==True and 'IPAddress' in j:
                current_time = datetime.now().astimezone(pytz.timezone("Europe/Paris")).strftime('%Y-%m-%d %H:%M:%S')
                t.add_row([current_time,j['Name'],j['Key'],j['IPAddress']])

t.header=False
t.align='l'
t.border=False
with open("log.txt", "a") as file:
    file.write(str(t))
    file.write("\n\n")
