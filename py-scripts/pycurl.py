'''
Developed by S. SHAJON
GitHub: github.com/SHAJON-404
Telegram: https://t.me/SHAJON
'''

import os
import requests

red = "\x1b[1;31m"
green = "\x1b[1;32m"
white = "\x1b[1;37m"
dflt = "\x1b[1;30m"

class Curl:
    URL = 10002
    POST = 100052
    HTTPHEADER = 10023
    POSTFIELDS = 10015
    SSL_VERIFYPEER = 64
    RESPONSE_CODE = 200
    EFFECTIVE_URL = 10023
    WRITEDATA = 10001
    COOKIE = 10022
    HTTPPOST = 10024
    FORM_FILE = 1
    FORM_CONTENTTYPE = 2
    FORM_FILENAME = 3
    VERBOSE = 41
    HEADER = 42
    NOPROGRESS = 43
    USERAGENT = 10018
    FOLLOWLOCATION = 52
    CUSTOMREQUEST = 10036
    TIMEOUT = 13
    CONNECTTIMEOUT = 78
    COOKIEFILE = 10031
    COOKIEJAR = 10082
    HEADERFUNCTION = 20079
    WRITEFUNCTION = 20011
    READFUNCTION = 20012

    def __init__(self):
        self.options = {}
        self.headers = []
        self.data = None
        self.ssl_verify = True
        self.method = "GET"
        self.write_data = None
        self.response = None
        self.cookie = None
        self.httppost = None

    def setopt(self, option, value):
        if option == self.HTTPHEADER:
            self.headers = value
        elif option == self.URL:
            self.options["url"] = value
        elif option == self.POSTFIELDS:
            self.data = value
            self.method = "POST"
        elif option == self.POST:
            if value == 1:
                self.method = "POST"
        elif option == self.SSL_VERIFYPEER:
            self.ssl_verify = bool(value)
        elif option == self.WRITEDATA:
            self.write_data = value
        elif option == self.COOKIE:
            self.cookie = value
        elif option == self.HTTPPOST:
            self.httppost = value
            self.method = "POST"
        else:
            self.options[option] = value

    def perform(self):
        url = self.options.get("url", "unknown URL")
        print(f"{white}-"*58)
        print(f"{green}SHAJON URL{red}: {dflt}{url}")
        print(f"{white}-"*58)
        print(f"{green}REQUEST METHOD{red}: {dflt}{self.method}")
        print(f"{white}-"*58)
        
        headers_dict = {}
        if self.headers:
            for header in self.headers:
                if ":" in header:
                    key, value = header.split(":", 1)
                    headers_dict[key.strip()] = value.strip()

        if self.cookie:
            headers_dict["Cookie"] = self.cookie

        if headers_dict:
            print(f"{green}SHAJON HEADERS{red}: {dflt}{headers_dict}")
            print(f"{white}-"*58)

        if self.data:
            print(f"{green}SHAJON DATA{red}: {dflt}{self.data}")
            print(f"{white}-"*58)

        if self.httppost:
            print(f"{green}SHAJON HTTPPOST{red}: {dflt}{self.httppost}")
            print(f"{white}-"*58)

        files = {}
        form_data = {}
        opened_files = []

        if self.httppost:
            for item in self.httppost:
                field_name, field_val = item[0], item[1]
                if isinstance(field_val, tuple) and len(field_val) >= 2 and field_val[0] == self.FORM_FILE:
                    file_path = field_val[1]
                    if os.path.exists(file_path):
                        f = open(file_path, "rb")
                        opened_files.append(f)
                        files[field_name] = (os.path.basename(file_path), f)
                    else:
                        files[field_name] = (file_path, b"")
                else:
                    form_data[field_name] = field_val

        try:
            if self.method == "POST":
                if self.httppost:
                    self.response = requests.post(url, headers=headers_dict if headers_dict else None, data=form_data, files=files if files else None, verify=self.ssl_verify)
                else:
                    self.response = requests.post(url, headers=headers_dict if headers_dict else None, data=self.data, verify=self.ssl_verify)
            else:
                self.response = requests.get(url, headers=headers_dict if headers_dict else None, verify=self.ssl_verify)
        finally:
            for f in opened_files:
                f.close()

        if self.write_data:
            self.write_data.write(self.response.text.encode('utf-8'))

    def getinfo(self, info_type):
        if info_type == self.RESPONSE_CODE:
            return self.response.status_code if self.response else None
        elif info_type == self.EFFECTIVE_URL:
            return self.options.get("url", "unknown URL")
        else:
            return None

    def close(self):
        pass


URL = Curl.URL
POST = Curl.POST
HTTPHEADER = Curl.HTTPHEADER
POSTFIELDS = Curl.POSTFIELDS
SSL_VERIFYPEER = Curl.SSL_VERIFYPEER
RESPONSE_CODE = Curl.RESPONSE_CODE
EFFECTIVE_URL = Curl.EFFECTIVE_URL
WRITEDATA = Curl.WRITEDATA
COOKIE = Curl.COOKIE
HTTPPOST = Curl.HTTPPOST
FORM_FILE = Curl.FORM_FILE
FORM_CONTENTTYPE = Curl.FORM_CONTENTTYPE
FORM_FILENAME = Curl.FORM_FILENAME
VERBOSE = Curl.VERBOSE
HEADER = Curl.HEADER
NOPROGRESS = Curl.NOPROGRESS
USERAGENT = Curl.USERAGENT
FOLLOWLOCATION = Curl.FOLLOWLOCATION
CUSTOMREQUEST = Curl.CUSTOMREQUEST
TIMEOUT = Curl.TIMEOUT
CONNECTTIMEOUT = Curl.CONNECTTIMEOUT
COOKIEFILE = Curl.COOKIEFILE
COOKIEJAR = Curl.COOKIEJAR
HEADERFUNCTION = Curl.HEADERFUNCTION
WRITEFUNCTION = Curl.WRITEFUNCTION
READFUNCTION = Curl.READFUNCTION