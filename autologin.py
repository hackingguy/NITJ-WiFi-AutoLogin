#!/usr/bin/env python3
import gi
gi.require_version('Notify', '0.7')
import requests
from gi.repository import Notify
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
req = requests.session()

login_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '74',
    'Origin': 'https://10.10.11.1:8090',
    'DNT': '1',
    'Connection': 'close',
    'Referer': 'http://10.10.11.1:8090/'
}

live_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'close',
    'Referer': 'http://10.10.11.1:8090/'
}

json_data = {
    'mode': '191',
    'username': '18104005',
    'password': '18104005',
    'a': '1578496066016',
    'producttype': '0'
}


def login(username, pwd):
    json_data["a"] = int(round(time.time() * 1000))
    try:
        try:
            r = req.post("http://10.10.11.1:8090/login.xml", json_data, headers=login_headers, verify=False)
        except:
            r = req.post("https://10.10.11.1:8090/login.xml", json_data, headers=login_headers, verify=False)
        response = r.content
        print(response.decode())
        if (b"signed" in response):
            Notify.init("NITJ WiFi AutoLogin")
            Notify.Notification.new("Login Successful").show()
            live_mode()
        elif (b"maximum" in response):
            Notify.init("NITJ WiFi AutoLogin")
            Notify.Notification.new("Maximum Login Limit").show()
        else:
            Notify.init("NITJ WiFi AutoLogin")
            Notify.Notification.new("Wrong Credentials").show()
    except:
        Notify.init("NITJ WiFi AutoLogin")
        Notify.Notification.new("Turn On WiFi").show()


def live_mode():
    try:
        while (True):
            time.sleep(10)
            url = "http://10.10.11.1:8090/live?mode=192&username="+json_data["username"]+"&a=" + str(
                int(round(time.time() * 1000))) + "&producttype=0"
            r = req.get(url, headers=live_headers, verify=False)
            response = r.content
            print(url+"\n"+response.decode())
            if(b"exceeded," in response):
                Notify.init("NITJ WiFi AutoLogin")
                Notify.Notification.new("Changing Account Data Limit Exceeded").show()
                break
    except:
        Notify.init("NITJ WiFi AutoLogin")
        Notify.Notification.new("Error Occured! Try Again").show()
    pass


login("18104005", "18104005")

