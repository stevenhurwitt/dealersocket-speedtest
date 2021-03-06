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
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import datetime as dt
import json
import math
import ast
import os

#driver = webdriver.Chrome(ChromeDriverManager().install())
base = "F:\\la-tools-test\\IDR_Drop"

def read_logins(file):
    
    try:
        good = pd.read_excel(file)
    except:
        good = file
        
    accts = [ast.literal_eval(a) for a in good.accts]
    output = []

    for i, row in enumerate(accts):
        n = len(row)
        groups = math.ceil(n // 4)
        old_row = [('date', good.date[i]), ('name', good.name[i]), ('user', good.user[i]), ('pw', good.pw[i]), ('util', good.util[i])]
    
        if (groups > 0) and (n % 4 != 0):
            
            for group in range(0, groups + 1):
                
                start = group*4
                end = (group + 1)*4
                temp_acct = row[start:end]
                
                new_acct = ('accts', temp_acct)
                old_row.append(new_acct)
                output.append(dict(old_row))
        
        elif (groups > 0) and (n % 4 == 0):
            
            for group in range(0, groups):
                
                start = group*4
                end = (group + 1)*4
                temp_acct = row[start:end]
                
                new_acct = ('accts', temp_acct)
                old_row.append(new_acct)
                output.append(dict(old_row))
                
        else:
            new_acct = ('accts', row)
            old_row.append(new_acct)
            output.append(dict(old_row))
        
        #output.append(dict(old_row))
    
    output_df = pd.DataFrame(output)
    output_df = output_df[['accts', 'date', 'name', 'user', 'pw', 'util']]
    return(output_df)

def past_days(good, n):
    
    good['date'] = pd.to_datetime(good['date'])
    past = dt.datetime.today() - dt.timedelta(days = n)
    past_good = good.iloc[[d > past for d in good.date],:]
    past_good.reset_index(drop = True, inplace = True)
    return(past_good)

def acct_match(table_acct, str_acct):
    parse = table_acct.split(' ')
    
    if len(parse) > 1:
        table_acct = ''.join(parse)
        
    return((table_acct in str_acct) or (str_acct in table_acct))

def big_match(str_acct, table):
    
    linking = []
    for row in table.findAll('tr'):
        cells = row.findAll('td')
        account = cells[1].find(text = True)
        
        if acct_match(account, str_acct):
            cells[0].input['selected'] = 'true'
            found = cells[0].input['value']
            
            linking.append(found)

    return linking

def check_the_box(value, browser):
    checkboxes = browser.find_elements_by_xpath("//input[@type='checkbox']")

    for checkbox in checkboxes:
        if checkbox.get_attribute('value') == value:
            checkbox.click()

def bodies_json(bodies):

    test = pd.DataFrame.from_dict(bodies, orient = 'index')

    if type(test.date[0]) == str:
            test.date = pd.to_datetime(test.date)

    accts_success = [len(accts) > 0 for accts in test.accts]
    accts_fail = [not val for val in accts_success]
        
    good = test[accts_success].reset_index(drop = True)
    util = []
    
    for i, a in enumerate(good.accts):
        first_acct = a[0]
        leading = a[0][:2]
        
        if leading == '80':
            util.append('PSNH')
            
        elif leading == '51' and (len(first_acct.split('_')) > 1):
            util.append('CLP')
            
        elif leading == '54' and (len(first_acct.split('_')) > 1):
            util.append('WMECO')
                
        else:
            if 'SUEZ' in good.user[i]:
                util.append('NGRID')
                
            else:
                util.append('NSTAR')
            
    good['util'] = util
        

    email_error = []

    if len(accts_fail) > 0:
        bad = test[accts_fail].reset_index()
        mail_error = 'EMAIL_SCRAPE_ERROR.csv'

        bad.to_csv(mail_error, header = True, index = False)

    return(good)

### Submit Login Info

def logon(username, pw, ngrid):

    opts = Options()
    #opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--ignore-certificate-errors')
    opts.add_argument('--start-maximized')
    opts.add_argument('--disable-dev-shm-usage')
    #opts.binary_location = '/usr/bin/google-chrome-stable'
    download_path = '/media/steven/big_boi/la-tools-test/IDR_Drop/Downloads'
    prefs = {
                'download.default_directory': download_path,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': False,
                'safebrowsing.disable_download_protection': True}
    #prefs ={"profile.default_content_settings.popups": 0, "download.default_directory": "/home/jupyter-engiela/la-tools-test/IDR_Drop/Downloads/", "directory_upgrade": True}
    opts.add_experimental_option("prefs", prefs)
    #assert opts.headless

    #setup headless browser, get ngrid url
    browser = Chrome(executable_path = 'F:\\la-tools-test\\IDR_Drop\\chromedriver.exe', options = opts)
    
    def enable_download_headless(browser,download_dir):
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        browser.execute("send_command", params)
    
    enable_download_headless(browser, download_path)
    
    if ngrid == True:
        url = 'https://ngrid.epo.schneider-electric.com/ngrid/cgi/eponline.exe'
        #url = 'https:\\ngrid.epo.schneider-electric.com\\ngrid\\cgi\\eponline.exe'
        
    if ngrid == False:
        url = 'https://eversource.epo.schneider-electric.com/eversource/cgi/eponline.exe'
        #url = 'https:\\eversource.epo.schneider-electric.com\\eversource\\cgi\\eponline.exe'

    browser.get(url)
       
    #see all elements on pg
    #ids = browser.find_elements_by_xpath('//*[@id]')

    ##Login Page
    #store username, pw, etc
    #send values to login
    #try:
    wait = ui.WebDriverWait(browser,10)
    wait.until(lambda browser: browser.find_element_by_id('userid'))
    
    user = browser.find_element_by_id('userid')
    password = browser.find_element_by_id('password')
    login = browser.find_element_by_id('contin')

    #except:
        #user = browser.find_element_by_xpath("\\div[@id='login']\\ul[@class='form row-fluid']\\li[@class='col-xs-12 col-sm-6']")
        #password = browser.find_element_by_xpath(".ul.form.row-fluid.li.col-xs-12.col-sm-6[input.id = password]")
        #login = browser.find_element_by_xpath(".ul.form.row-fluid.li.col-xs-12.col-sm-6[input.id = contin]")

    user.send_keys(username)
    password.send_keys(pw)

    #sanity check
    print('user: ', user.get_attribute('value'))
    print('password: ', password.get_attribute('value'))
    login.click()
    browser.execute_script('''function submitlogin(event) {document.frmEPO.submit();}''' )
    wait = ui.WebDriverWait(browser,10)
    wait.until(lambda browser: browser.find_element_by_id('LastNDays'))

    ##Accounts Page
    #set recent days to be 400
    #could config to use dates....
    lastndays = browser.find_element_by_id('LastNDays')

    #browser.execute_script("arguments[0].value = '400';", recdays)
    browser.execute_script("arguments[0].value = '400'", lastndays)

    print('set to last ', lastndays.get_attribute('value'), ' days.')
    browser.execute_script("document.getElementById('LastNDays').focus();")
    
    wait = ui.WebDriverWait(browser,10)
    pass
    
    return(browser, url)

def idr_download(user, pw, accts_to_find):

    ngrid = ('SUEZ' in user)
    browser, url = logon(user, pw, ngrid)
    print('logging on...')

    #accts_to_find = good.accts[row]
    print('looking for {} accts.'.format(len(accts_to_find)))
    AIDs = []

    soup = BeautifulSoup(browser.page_source, features = 'html5lib')
    table = soup.find('tbody', {'role' : 'rowgroup'})
    
    if table:
        print('found items in portal.')
    
    else:
        print('login error.')

    #get EPO AID value for every account
    print('trying search & download...')
    print('')
    
    for accts in accts_to_find:
        
        results = big_match(accts, table)
        AIDs.append(results[0])
 
    browser.implicitly_wait(2)
    
    file = export_data(AIDs, browser, ngrid)                      
           
    return(file)

def export_data(list_of_4, browser, ngrid):
    
    if (len(list_of_4) > 1) and ngrid == False:
        for item in list_of_4:
            check_the_box(item, browser)
            
            
    elif (len(list_of_4) > 1) and ngrid == True:
        for item in list_of_4:
            check_the_box(item, browser)
    
    browser.execute_script('''document.frmEPO.button.value='export'; document.frmEPO.submit();''')

    browser.implicitly_wait(20)

    
    #print('disabling demand...')
    browser.execute_script('''function disabledemand() {if (document.frmEPO.demand) {
		document.frmEPO.demand.disabled=true;
		document.frmEPO.demand.checked=false;}}; disabledemand''')
            
    #print('selecting hourly interval...')
    browser.execute_script('''function setintervaltype() {if (document.frmEPO.demand && document.frmEPO.intervaltype[0]) {
	if ( document.frmEPO.demand.checked == true ) {
	if ( document.frmEPO.intervaltype[1].checked == true ) {alert("Convert to Demand can only be selected with the Native Interval Length. [Un-check Convert to Demand if Hourly data is desired]");}
	    document.frmEPO.intervaltype[0].checked = true;
	    document.frmEPO.intervaltype[1].checked = false;
	    document.frmEPO.intervaltype[0].disabled = true;
	    document.frmEPO.intervaltype[1].disabled = true;}
	else {document.frmEPO.intervaltype[0].disabled = false;
	    document.frmEPO.intervaltype[1].disabled = false;
	    document.frmEPO.intervaltype[1].checked = true;
	    document.frmEPO.intervaltype[0].checked = false;}}}; setintervaltype()''')

    print('submitting...')
    browser.execute_script('''document.frmEPO.button.value="contin"''')
    browser.execute_script('''document.frmEPO.submit();''')

    browser.implicitly_wait(20)
    link = browser.find_element_by_partial_link_text('Hourly Data File') 
    url = link.get_attribute('href')
    
    url = urlparse(url)
    path = url.path

    url_split = path.split('/')
    file = url_split[len(url_split) - 1]  

    link.click()
    browser.implicitly_wait(5)
    print('downloaded EPO data file {}.'.format(file))
    
    browser.back()
    browser.back()
    
    for item in list_of_4:
        check_the_box(item, browser)
     
    return(file)