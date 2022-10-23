#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import json
import pendulum
import requests
from tabulate import tabulate


df = pd.DataFrame({'Name':['Diaa','Sameh']})


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
    
    
send_chime(df)

