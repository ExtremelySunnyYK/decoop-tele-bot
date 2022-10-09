import requests
import numpy as np 
import pandas as pd 
import datetime as dt 
import requests

def get_credit_score(address):
    """Makes a post request to url with post data as address and returns the credit score of the address"""
    url = "https://decoop.vercel.app/api/credit_score"
    post_data = {"address": address}
    response = requests.post(url, json=post_data)
    return response.json()

# def credit_score(address, contract_pool):

#     link = 'https://api-goerli.etherscan.io/api?module=account&action=tokentx&address=' + address + '&startblock=0&endblock=99999999&sort=asc&apikey=DI8JFV4AEBPKDPYTKEK8B5PCQXD2YUN75E'
#     data = requests.get(link).json()['result']
#     df = pd.DataFrame(data)
#     df['timeStamp'] = df.timeStamp.apply(lambda x: dt.datetime.utcfromtimestamp(int(x)))
#     df = df[['timeStamp', 'from', 'to','value']]
#     df['value'] = df['value'].astype(float)/10**18
#     df['Deposit'] = (df['from'] == address) & (df['to'] == contract_pool)
#     df['Withdraw'] = (df['from'] == contract_pool) & (df['to'] == address)
    
#     deposited_amount = 0 
#     withdrawn_amount = 0 
#     for i in range(len(df)): 
#         if df.loc[i, 'Deposit'] == True: 
#             deposited_amount += df.loc[i, 'value']
#         if df.loc[i, 'Withdraw'] == True: 
#             withdrawn_amount += df.loc[i, 'value']

#     credit_score = min(deposited_amount, withdrawn_amount)
    
#     return credit_score

if __name__ == "__main__":
    print(credit_score("0xAD2d2CDE7CA8d116d545099405C1FDFc57B6FD9e"))