import requests
import numpy as np 
import pandas as pd 
import datetime as dt 

def credit_score(address, contract_pool):

    link = 'https://api.etherscan.io/api?module=account&action=tokentx&address=' + address + '&startblock=0&endblock=99999999&sort=asc&apikey=DI8JFV4AEBPKDPYTKEK8B5PCQXD2YUN75E'
    data = requests.get(link).json()['result']
    df = pd.DataFrame(data)
    df['timeStamp'] = df.timeStamp.apply(lambda x: dt.datetime.utcfromtimestamp(int(x)))
    df = df[['timeStamp', 'from', 'to','value']]
    df['value'] = df['value'].astype(float)/10**18
    df['Deposit'] = (df['from'] == address) & (df['to'] == contract_pool)
    df['Withdraw'] = (df['from'] == contract_pool) & (df['to'] == address)
    
    deposited_amount = 0 
    for i in range(len(df)): 
        if df.loc[i, 'Deposit'] == True: 
            deposited_amount += df.loc[i, 'value']

    withdrawn_amount = 0 
    for i in range(len(df)): 
        if df.loc[i, 'Withdraw'] == True: 
            withdrawn_amount += df.loc[i, 'value']

    credit_score = min(deposited_amount, withdrawn_amount)
    
    return credit_score