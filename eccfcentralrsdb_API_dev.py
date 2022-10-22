#!/usr/bin/env python
# coding: utf-8

# In[ ]:


url_now = 'https://monitorportal.amazon.com/mws/data?Action=GetGraph&Version=2007-07-07&SchemaName1=Service&DataSet1=Prod&Marketplace1=CascadesAllocatorService%3Aprod%3AUSAmazon&HostGroup1=ALL&Host1=ALL&ServiceName1=CascadesAllocatorService&MethodName1=ALL&Client1=ALL&MetricClass1=NONE&Instance1=NONE&Metric1=eccfcentralrsdb%3Atotal%3Apending&Period1=OneMinute&Stat1=p100&LiveData1=true&Label1=Job%20Runs%20currently%20Waiting%20for%20resources&UserLabel1=Job%20Runs%20currently%20Waiting%20for%20resources&SchemaName2=Service&Metric2=eccfcentralrsdb%3Atotal%3Aallocated&YAxisPreference2=right&Label2=Job%20Runs%20currently%20Executing&UserLabel2=Job%20Runs%20currently%20Executing&HeightInPixels=1130&WidthInPixels=1517&GraphTitle=eccfcentralrsdb%20WaitingForResources%20vs.%20Executing&TZ=Africa%2FCairo@TZ%3A%20Cairo&LabelLeft=Job%20Runs&VerticalLine1=MCM-7465630%20-%20@%202017%2F11%2F08%2011%3A18am%2C&StartTime1=-PT1M&EndTime1=-PT0M'
#url_7_days = 'https://monitorportal.amazon.com/mws/data?Action=GetGraph&Version=2007-07-07&SchemaName1=Service&DataSet1=Prod&Marketplace1=CascadesAllocatorService%3Aprod%3AUSAmazon&HostGroup1=ALL&Host1=ALL&ServiceName1=CascadesAllocatorService&MethodName1=ALL&Client1=ALL&MetricClass1=NONE&Instance1=NONE&Metric1=eccfcentralrsdb%3Atotal%3Apending&Period1=OneHour&Stat1=p100&LiveData1=true&Label1=Job%20Runs%20currently%20Waiting%20for%20resources&UserLabel1=Job%20Runs%20currently%20Waiting%20for%20resources&SchemaName2=Service&Metric2=eccfcentralrsdb%3Atotal%3Aallocated&YAxisPreference2=right&Label2=Job%20Runs%20currently%20Executing&UserLabel2=Job%20Runs%20currently%20Executing&HeightInPixels=1130&WidthInPixels=1517&GraphTitle=eccfcentralrsdb%20WaitingForResources%20vs.%20Executing&TZ=UTC@TZ%3A UTC&LabelLeft=Job%20Runs&VerticalLine1=MCM-7465630%20-%20@%202017%2F11%2F08%2011%3A18am%2C&StartTime1=-P7D&EndTime1=-P1D' #&TZ=Asia%2FDubai@TZ%3A%20Dubai& / &TZ=UTC@TZ%3A UTC&
url_15_mins = 'https://monitorportal.amazon.com/mws/data?Action=GetGraph&Version=2007-07-07&SchemaName1=Service&DataSet1=Prod&Marketplace1=CascadesAllocatorService%3Aprod%3AUSAmazon&HostGroup1=ALL&Host1=ALL&ServiceName1=CascadesAllocatorService&MethodName1=ALL&Client1=ALL&MetricClass1=NONE&Instance1=NONE&Metric1=eccfcentralrsdb%3Atotal%3Apending&Period1=FiveMinute&Stat1=p100&LiveData1=true&Label1=Job%20Runs%20currently%20Waiting%20for%20resources&UserLabel1=Job%20Runs%20currently%20Waiting%20for%20resources&SchemaName2=Service&Metric2=eccfcentralrsdb%3Atotal%3Aallocated&YAxisPreference2=right&Label2=Job%20Runs%20currently%20Executing&UserLabel2=Job%20Runs%20currently%20Executing&HeightInPixels=1130&WidthInPixels=1517&GraphTitle=eccfcentralrsdb%20WaitingForResources%20vs.%20Executing&TZ=Africa%2FCairo@TZ%3A%20Cairo&LabelLeft=Job%20Runs&VerticalLine1=MCM-7465630%20-%20@%202017%2F11%2F08%2011%3A18am%2C&StartTime1=-PT15M&EndTime1=-PT0M'

import requests
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None  # default='warn' // to hide the error: SettingWithCopyWarning
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from urllib3.exceptions import InsecureRequestWarning #from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
req = requests.Session()
from datetime import datetime, timedelta
dt = datetime.now() + timedelta(hours=2)
dt_string = str(dt.strftime("%Y-%m-%d %H:%M"))
import datetime
year = datetime.datetime.now().date().year
#dt_string
import json
import pendulum
from tabulate import tabulate
from time import sleep

def send_chime(df):
    webhook_url = f'https://hooks.chime.aws/incomingwebhooks/590459e3-331d-4cb7-82af-8b9136130490?token=MzZMampLc1Z8MXxrdmZJQTJyeE5EQU5OLVloTGQ0TWtEWHBKYmFRWlZpVHBTUE5MR0M2Q0lr'
    kwargs = {"tablefmt": "github", "headers": "keys", "showindex": False}
    mark_down = tabulate(df, **kwargs)
    message = (
    f"/md " + "\n"       #Add Members & write your message!
    + f"{mark_down}"
    )

    req = requests.Session()
    payload = {"Content": message}
    header = {"Content-Type": "application/json"}
    req.post(webhook_url, json=payload, headers=header)

    
while True:

    d_len = 0
    while d_len < 5:
        try:
            sleep(2)
            
            #get_data
            nn = req.get(url_now, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False).content
            mm = req.get(url_15_mins, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False).content
            #hh = req.get(url_7_days, auth=HTTPKerberosAuth(mutual_authentication=OPTIONAL), verify=False).content
            
            now = pd.read_html(nn)[-1]
            avg_15_mins = pd.read_html(mm)[-1]
            
            print(now)
            d_len = np.int64(len(now.columns))
            
            if now.isnull().values.any():
                d_len = 0
            else:
                pass
            
        except:
             pass   

    now.drop(labels=['Min','Avg','Max'], axis=1, inplace=True)
    now.rename(columns={ 'Label': 'Job Runs', now.columns[1]: dt_string }, inplace = True)
    #now

    avg_15_mins = avg_15_mins[['Label','Avg']]
    avg_15_mins.rename(columns={ 'Avg': 'Average last 15 minutes' }, inplace = True)
    #avg_15_mins

    result = pd.concat([now, avg_15_mins['Average last 15 minutes']], axis=1, join='inner')
    result.loc[result['Job Runs'] == 'Job Runs currently Executing', "Job Runs"] = 'Executing'
    result.loc[result['Job Runs'] == 'Job Runs currently Waiting for resources', "Job Runs"] = 'Waiting for resources'
    result['Average last 15 minutes'] = result['Average last 15 minutes'].astype('int64')
    result.iloc[:, 1] = result.iloc[:, 1].astype('int64') #dt_string to int64

    result['🤖'] = np.where(result[dt_string] < result['Average last 15 minutes'], '🟢', np.where(result[dt_string] > result['Average last 15 minutes'], '🔴', '🟡'))
    result = result[['Job Runs','🤖',dt_string,'Average last 15 minutes']]
    #result

    send_chime(result)
    
    sleep(60)


# In[ ]:





# In[ ]:





# In[ ]:




