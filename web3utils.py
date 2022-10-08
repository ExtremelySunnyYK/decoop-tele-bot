import logging
from web3 import Web3
from dotenv import load_dotenv
import os
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv("keys.env")
token = str(os.getenv("RPC_KEY"))

CommunityAddress = "0x6DCFC2BD7Ee97386d080209549eBE61D98d3fD6A"
FactoryAddress = "0xC8Ee6F2d24A9D6718F2068D5Ee7a99880284495f"
ERC20Address = "0xAAc502bcf03D977D7Ca21ee4C28D8981Ec9E3d71"

def build_create_community_tx(name):
    w3 = get_web3()
    factory_contract = get_factory_contract()
    # Build the transaction
    tx = factory_contract.functions.create(name).buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    print(tx)
    return tx

def build_join_community_tx():
    w3 = get_web3()
    community_contract = get_community_contract()
    # Build the transaction
    tx = community_contract.functions.joinCommunity().buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    print (tx)
    return tx

def build_deposit_tx(amount):
    w3 = get_web3()    
    # build a transaction that sends erc20 from the user's account to the community fund
    erc20_contract = get_erc_20_contract()
    tx = erc20_contract.functions.transfer(CommunityAddress, amount).buildTransaction({
        'chainId': 5,
        'gas': 1000000,
        'gasPrice': w3.toWei('50', 'gwei'),
    })
    print (tx)
    return tx

def get_erc_20_contract():
    with open('./abi/erc20.json') as f:
        erc20_abi = json.load(f)
    
    w3 = get_web3()
    erc20_contract = w3.eth.contract(address=ERC20Address, abi=erc20_abi)
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
    community_contract = w3.eth.contract(address=CommunityAddress, abi=community_abi)
    return community_contract

def get_factory_contract():
    with open('./abi/factory.json') as f:
        factory_abi = json.load(f)
    
    w3 = get_web3()
    factory_contract = w3.eth.contract(address=FactoryAddress, abi=factory_abi)
    return factory_contract

def getUsdcBalance(address):
    """Get the USDC balance of an address"""
    w3 = get_web3()
    # Get balance
    balance = w3.eth.getBalance(address)
    
    # convert balance to ether
    ether = w3.fromWei(balance, 'ether')
    return ether


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
    build_deposit_tx(0.1)