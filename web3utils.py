import logging
from web3 import Web3
from dotenv import load_dotenv
import os
import json

from credit_score import credit_score

from utils import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv("keys.env")
token = str(os.getenv("RPC_KEY"))

FactoryAddress = "0xE372F4B9aA4689a244a1066F8296d32108141A69"


def build_create_community_tx(name):
    w3 = get_web3()
    factory_contract = get_factory_contract()
    # Build the transaction
    tx = factory_contract.functions.create(name).buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    return format_call_data(tx)

def build_join_community_tx():
    w3 = get_web3()
    community_contract = get_community_contract()

    # Build the transaction
    tx = community_contract.functions.joinCommunity().buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    print(tx)
    return format_call_data(tx)

def build_deposit_tx(amount):
    w3 = get_web3()    
    # build a transaction that sends erc20 from the user's account to the community fund
    erc20_contract = get_erc_20_contract()
    # convert address to checksum address
    address = w3.toChecksumAddress(get_newest_community_address())

    # convert amount to wei
    amount = w3.toWei(amount, 'ether')

    tx = erc20_contract.functions.transfer(address, amount).buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    return format_call_data(tx)

def build_withdraw_tx(amount):
    w3 = get_web3()
    community_contract = get_community_contract()

    # convert amount to wei
    amount = w3.toWei(amount, 'ether')
    
    # Build the transaction
    tx = community_contract.functions.withdraw(amount).buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    return format_call_data(tx)

def get_erc_20_contract():
    with open('./abi/erc20.json') as f:
        erc20_abi = json.load(f)
    
    w3 = get_web3()
    erc20_contract = w3.eth.contract(address=get_community_token_address(), abi=erc20_abi)
    return erc20_contract

def get_web3():
    # Create a Web3 object
    w3 = Web3(Web3.HTTPProvider(token))
    return w3

def get_balance(address):
    w3 = get_web3()
    # Get balance
    balance = w3.eth.getBalance(address)
    
    # convert balance to ether
    ether = w3.fromWei(balance, 'ether')
    return str(ether) + "eth"

def get_community_contract():
    with open('./abi/community.json') as f:
        community_abi = json.load(f)
    
    w3 = get_web3()
    community_contract = w3.eth.contract(address=get_newest_community_address(), abi=community_abi)
    return community_contract

def get_factory_contract():
    with open('./abi/factory.json') as f:
        factory_abi = json.load(f)
    
    w3 = get_web3()
    factory_contract = w3.eth.contract(address=FactoryAddress, abi=factory_abi)
    return factory_contract

def get_newest_community_address():
    factory_contract = get_factory_contract()
    index = factory_contract.functions.lastIndex().call() - 1
    communities = factory_contract.functions.communities(index).call()
    print(communities)
    return communities

def get_community_name():
    community_contract = get_community_contract()
    name = community_contract.functions.name().call()
    return name

def get_community_token_address():
    community_contract = get_community_contract()
    erc20_address = community_contract.functions.communityToken().call()
    return erc20_address

def get_community_sbt_address():
    community_contract = get_community_contract()
    sbt_address = community_contract.functions.soulboundToken().call()
    return sbt_address

def getUsdcBalance(address):
    """Get the USDC balance of an address"""
    w3 = get_web3()
    # Get balance
    balance = w3.eth.getBalance(address)
    
    # convert balance to ether
    ether = w3.fromWei(balance, 'ether')
    return ether

def get_credit_score(address):
    community_address = get_newest_community_address()
    score = credit_score(address, community_address)
    return score


def test_connection():
    w3 = get_web3()
    # Check if connected to Ethereum
    if w3.isConnected():
        print("Connected to Ethereum")
    else:
        print("Not connected to Ethereum")

if __name__ == "__main__":
    # print(get_balance("0xD93Bcd514471730a7B5C3052dA61e8EE4D7415B0"))
    # build_create_community_tx("test")
    # build_join_community_tx()
    # build_deposit_tx(0.1)
    # get_communities()
    # print(build_create_community_tx("test"))
    # print(build_join_community_tx())
    # print(build_deposit_tx(0.11))
    print(build_withdraw_tx(0.1))
    get_credit_score("0xAD2d2CDE7CA8d116d545099405C1FDFc57B6FD9e")
    # generate_qr_code(build_join_community_tx())
