# http://speedtest.dealersocket.com/
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import selenium.webdriver as webdriver
try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    print('webdriver_manager import error can suck my cock.')
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import datetime as dt
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import requests 
import pprint
import time
import json
import math
import uuid
import sys
import ast
import re
import os

base = os.getcwd()
pp = pprint.PrettyPrinter(indent = 1)
print("imported modules successfully.")

def logon():
    """
    function to logon to webpage
    arguments: None
    returns: browser
    """

    opts = Options()
    #opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--start-maximized')
    opts.add_argument('--disable-dev-shm-usage')
    #opts.binary_location = '/usr/bin/google-chrome-stable'
    download_path = os.getcwd()
    prefs = {
                'download.default_directory': download_path,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': False,
                'safebrowsing.disable_download_protection': True
            }
    #prefs ={"profile.default_content_settings.popups": 0, "download.default_directory": "/home/jupyter-engiela/la-tools-test/IDR_Drop/Downloads/", "directory_upgrade": True}
    opts.add_experimental_option("prefs", prefs)
    #assert opts.headless

    #setup headless browser, get url
    try:
        browser = Chrome(executable_path = 'chromedriver', options = opts)

    except:
        raise Exception("couldn't start chromedriver.")
    
    def enable_download_headless(browser,download_dir):
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        browser.execute("send_command", params)
    
    try:
        enable_download_headless(browser, download_path)

    except:
        raise Exception("for browser, {}".format(download_path))

    url = "https://speedtest.dealersocket.com"
    #url = "https:\\ngrid.epo.schneider-electric.com\\ngrid\\cgi\\eponline.exe"

    browser = browser.get(url)
    # print(str(type(result)))

    return(browser)
    

def main():
    """
    main function
    arguments:
    returns:
    """
    opts = Options()
    #opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--start-maximized')
    opts.add_argument('--disable-dev-shm-usage')
    #opts.binary_location = '/usr/bin/google-chrome-stable'
    download_path = os.getcwd()
    prefs = {
                'download.default_directory': download_path,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': False,
                'safebrowsing.disable_download_protection': True
            }
    #prefs ={"profile.default_content_settings.popups": 0, "download.default_directory": "/home/jupyter-engiela/la-tools-test/IDR_Drop/Downloads/", "directory_upgrade": True}
    opts.add_experimental_option("prefs", prefs)
    #assert opts.headless

    browser = Chrome(executable_path = 'chromedriver', options = opts)
    
    def enable_download_headless(browser,download_dir):
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        browser.execute("send_command", params)
    
    enable_download_headless(browser, download_path)

    url = "http://speedtest.dealersocket.com/"

    browser.get(url)

    start = browser.find_element_by_id("startBtn")
    start.click()
    # print(start)
    # browser.execute_script('''function submitlogin(event) {document.frmEPO.submit();}''' )
    # print(type(browser))
    # wait = ui.WebDriverWait(browser,10)
    # wait.until(lambda browser: browser.find_element_by_id('userid'))
    download = browser.find_element_by_id("ggdl")
    upload = browser.find_element_by_id("ggul")
    ping = browser.find_element_by_id("ggping")
    jitter = browser.find_element_by_id("ggjitter")

    print(download)

    # payload = {
    #                 "download": download,
    #                 "upload": upload,
    #                 "ping": ping,
    #                 "jitter": jitter
    #            }
    # pp.pprint(payload)
    # html = browser.page_source
    # soup = BeautifulSoup(html, 'html5lib')
    try:
        download = browser.find_element_by_xpath("/html/body/div[1]/div[1]/svg/text[2]")
        print(download)
    except:
        pass

    # with open("payload.json", "w") as f:
    #     json.dumps(str(payload))
        # json_payload.dump(f)

    print("tried to write payload.json")
    # BeautifulSoup(download, "html5lib")
    # print(soup.select_one("tspan[style*=webkit]").text)
    # start = browser.find_element_by_id("startBtn")
    # try:
    #     browser.execute("javascript:runTest()")
    # except:
    #     raise Exception("error loading browser.")
    # password = browser.find_element_by_id('password')
    # login = browser.find_element_by_id('contin')
    # print(my_result)
    # ...
    # ...

if __name__ == "__main__":
    main()