import re
import subprocess

import time

from client.config import *
import requests
from requests.exceptions import ConnectionError


class Sender():


    def get_ip(self, ifname=ADSL_IFNAME):
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if status == 0:
            pattern = re.compile(ifname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
            result = re.search(pattern, output)
            if result:
                ip = result.group(1)
                return ip


    def adsl(self):
        while True:
            print('ADSL Start, Please wait')
            adsl_status = requests.get(SERVER_URL+'/adsl_status')
            if adsl_status == 0:

                (status, output) = subprocess.getstatusoutput(ADSL_BASH)
                if status == 0:
                    print('ADSL Successfully')
                    ip = self.get_ip()
                    if ip:
                        print('New IP', ip)
                        try:
                            requests.post(SERVER_URL, data={'token': TOKEN, 'port': PROXY_PORT, 'name': CLIENT_NAME})
                            print('Successfully Sent to Server', SERVER_URL)
                        except ConnectionError:
                            print('Failed to Connect Server', SERVER_URL)
                        time.sleep(40)
                    else:
                        print('Get IP Failed')
                else:
                    print('ADSL Failed, Please Check')

            time.sleep(1)


def run():
    sender = Sender()
    sender.adsl()


if __name__ == '__main__':
    run()
